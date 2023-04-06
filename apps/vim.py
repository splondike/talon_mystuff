"""
Python code related to vim
"""

# Post equals dubquote

from typing import Dict, Any, Optional, Tuple
import re

from talon import actions, cron, ui, clip, Context, Module

mod = Module()

ctx = Context()
ctx.matches = r"""
title: /^VIM/i
"""

ctx_normal = Context()
ctx_normal.matches = r"""
title: /^VIM n/i
"""

ctx_insert = Context()
ctx_insert.matches = r"""
title: /^VIM i/i
"""

ctx_visual = Context()
ctx_visual.matches = r"""
title: /^VIM v/i
"""

mod.list("vim_text_object", desc="Text objects in vim")

ctx.lists["self.vim_text_object"] = {
    "word": "s w",
    "end": "$",
    "subscript": "s ]",
    "args": "s )",
    "brace": "s }",
    "angle": "s <",
    "string": "s '",
    "outer string": "a '",
    "dub string": "s \"",
    "outer dub string": "a \"",
    "item": "a a",
}


@mod.capture(
    rule="([abs] <digits>) | ([<digits>] [post] (<user.letter>+ | numb <user.number_key>+ | <user.symbol_key>) [(twice|thrice)])"
)
def vim_jump_position(m) -> Dict[str, Any]:
    """
    Position we can jump to.

    <user.digits> is the line number with abs or abbreviation thereof otherwise,
    'post' is to say jump after the token,
    then the options in parentheses are:
        * the first letters or numbers of a word/token.
        * a symbol key
    twice|thrice say to go to the second or third such match
    """

    if hasattr(m, "letter_list"):
        target_type = "word"
        target_chars = m.letter_list
    elif hasattr(m, "number_key_list"):
        target_type = "word"
        target_chars = m.number_key_list
    elif hasattr(m, "symbol_key"):
        target_type = "char"
        target_chars = [m.symbol_key]
    else:
        target_type = "none"
        target_chars = []

    repeated = 0
    if "twice" in m:
        repeated = 1
    elif "thrice" in m:
        repeated = 2

    return {
        "line": m.digits if hasattr(m, "digits") else -1,
        "line_is_absolute": "abs" in m,
        "is_post": "post" in m,
        "repeated": repeated,
        "target_type": target_type,
        "target_chars": target_chars
    }


@mod.capture(
    rule="<digits> | (<digits> (<user.letter>+ | numb <user.number_key>+ | <user.symbol_key>))"
)
def vim_bring_range(m) -> Dict[str, Any]:
    """
    Range we can bring to the current cursor location

    <user.digits> is the line number (or abbreviation thereof),
    then the options in parentheses are:
        * the first letters or numbers of a word/token.
        * a symbol key
    """

    if hasattr(m, "letter_list"):
        target_type = "word"
        target_chars = m.letter_list
    elif hasattr(m, "number_key_list"):
        target_type = "word"
        target_chars = m.number_key_list
    elif hasattr(m, "symbol_key"):
        target_type = "char"
        target_chars = [m.symbol_key]
    else:
        target_type = "none"
        target_chars = []

    return {
        "line": m.digits,
        "line_is_absolute": False,
        "is_post": False,
        "repeated": 0,
        "target_type": target_type,
        "target_chars": target_chars
    }


def _parse_title_data() -> Tuple[str, int, int]:
    title = actions.win.title()
    if not title.startswith("VIM"):
        raise RuntimeError("Called when VIM not focussed")

    _v, mode, line, col, max_lines, _ = title.split(" ", maxsplit=5)

    return (mode, int(line), int(col), int(max_lines))


def _calculate_smart_line(uttered_line, is_absolute, curr_line, max_lines) -> int:
    if is_absolute or uttered_line >= 100:
        return uttered_line

    curr_hundreds = 100 * (curr_line // 100)
    curr_rest = curr_line % 100

    if curr_rest == uttered_line:
        return curr_line

    base = curr_hundreds + uttered_line
    closest = None
    options = [base, base + 100, base - 100]
    for option in options:
        if option < 1 or option > max_lines:
            continue

        if closest is None or (abs(option - curr_line) < abs(closest - curr_line)):
            closest = option

    if closest is None:
        raise RuntimeError("Couldn't find line matching {uttered_line}")

    return closest


def _calculate_pos(
        text, target_type, target_chars,
        enable_iter=False, orig_col=1, repeated=0
        ) -> Optional[Tuple[int, int]]:

    if target_type == "none":
        return None

    if target_type == "char":
        matcher = "".join(target_chars)
        spans = []
        try:
            start_idx = 0
            while True:
                # +1 because col nums are 1-indexed
                idx = text.index(matcher, start_idx) + 1
                spans.append((idx, idx + len(matcher)))
                start_idx = idx
        except ValueError:
            pass
    elif target_type == "word":
        pattern = "(^|(?<=\\W))" + "".join(target_chars) + ".*?($|(?=\\W))"
        spans = []
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            spans.append((
                match.start() + 1,
                match.end() + 1
            ))
    else:
        return None

    if len(spans) == 0:
        return None

    matching_idx = 0
    for i, (start, _) in enumerate(spans):
        if not enable_iter or orig_col < start:
            matching_idx = i
            break

    return spans[matching_idx + repeated % len(spans)]


@mod.action_class
class VimActions:
    def vim_jump(target: Dict[str, Any]):
        """
        Jump to the given position
        """

        actions.user.vim_normal_mode()
        _, orig_line, orig_col, max_lines = _parse_title_data()

        if target["line"] != -1:
            target_line = _calculate_smart_line(
                target["line"],
                target["line_is_absolute"],
                orig_line,
                max_lines
            )
            is_same_line = target_line == orig_line
            line_str = str(target_line)
            actions.insert(f"{line_str}G")
        else:
            is_same_line = True

        if target["target_type"] == "none":
            return

        with clip.revert():
            actions.key("C")
            # There's a slight race condition with vim setting the clipboard
            # so give it a bit more margin for error
            actions.sleep("50ms")
            line_text = clip.text()
            maybe_pos = _calculate_pos(
                line_text,
                target["target_type"],
                target["target_chars"],
                is_same_line,
                orig_col,
                repeated=target["repeated"]
            )

        if maybe_pos is None:
            return

        pos = maybe_pos[1] if target["is_post"] else maybe_pos[0]
        _, _, curr_col, _ = _parse_title_data()

        # <num>| uses screen columns, which doesn't work with wrap, hence
        # press the relevant arrow key n times to move. Jumping to the
        # start of the line first produces annoying flicker, so do this
        # calculation from the current cursor pos
        diff = pos - curr_col
        if diff < 0:
            actions.insert(str(abs(diff)))
            actions.key("left")
        elif diff > 0:
            actions.insert(str(abs(diff)))
            actions.key("right")
        else:
            pass

    def vim_bring(target: Dict[str, Any]):
        """
        Bring the given range to the current cursor position
        """

        actions.user.vim_normal_mode()
        _, orig_line, orig_col, max_lines = _parse_title_data()

        if target["line"] != -1:
            target_line = _calculate_smart_line(
                target["line"],
                target["line_is_absolute"],
                orig_line,
                max_lines
            )
            is_same_line = target_line == orig_line
            line_str = str(target_line)
            actions.insert(f"{line_str}G")
        else:
            is_same_line = True

        if target["target_type"] == "none":
            actions.key("C")
            actions.sleep("500ms")
            actions.key("` `")
            actions.sleep("500ms")
            # TODO: I think edit.paste() is still using the insert mode context or something? Using this explicit key works better.
            actions.key("V")
        else:
            with clip.revert():
                actions.key("C")
                # There's a slight race condition with vim setting the clipboard
                # so give it a bit more margin for error
                actions.sleep("50ms")
                line_text = clip.text()
                maybe_pos = _calculate_pos(
                    line_text,
                    target["target_type"],
                    target["target_chars"],
                    is_same_line,
                    orig_col,
                    repeated=target["repeated"]
                )

                if maybe_pos is None:
                    return

                _, _, curr_col, _ = _parse_title_data()

                # TODO: Janky slow way of doing this. Should work out how to
                # either just insert the text or put it in the clipboard and
                # paste
                diff = maybe_pos[0] - curr_col
                if diff < 0:
                    actions.insert(str(abs(diff)))
                    actions.key("left")
                elif diff > 0:
                    actions.insert(str(abs(diff)))
                    actions.key("right")
                else:
                    pass
                actions.key("a")
                actions.key(f"right:{maybe_pos[1] - maybe_pos[0] - 1}")
                actions.key("c")
                actions.sleep("50ms")

                actions.key("` `")
                actions.edit.paste()


    def vim_normal_mode():
        """
        Change vim to normal mode
        """
        # TODO: Testing just always doing this since delays in Talon
        # context switching slows down chaining a bit
        actions.key("escape")
        # Can take vim a little to be ready for normal keys
        actions.sleep(0.1)

    def vim_select_rows(start_row: int, end_row: int = -1):
        """
        Selects rows start_row to end_row
        """
        if end_row == -1:
            smaller = start_row
            down_times = 0
        else:
            smaller = min(start_row, end_row)
            down_times = max(start_row, end_row) - smaller

        actions.key("escape")
        actions.insert(f":{smaller}")
        actions.key("enter")
        actions.key("shift-a")
        if down_times != 0:
            actions.key(f"down:{down_times}")


@ctx.action_class("edit")
class VimEditActions:
    def undo():
        actions.key("z")

    def redo():
        actions.key("shift-z")

    def paste():
        actions.key("V")

    def indent_more():
        actions.key("> >")

    def indent_less():
        actions.key("< <")

    def find(text: str = None):
        actions.user.vim_normal_mode()
        actions.key("/")
        if text:
            actions.insert(text)
            actions.key("enter")

    def find_next():
        actions.user.vim_normal_mode()
        actions.key("ctrl-i")


@ctx.action_class("win")
class VimWinActions:
    def file_ext():
        title = ui.active_window().title
        if not title.startswith("VIM"):
            # For some reason this gets called one final time
            # when swapping off the window
            return ""

        _, filename = title.rsplit(" ", 1)

        try:
            pos = filename.index(".")
            return filename[pos:]
        except ValueError:
            return ""


@ctx_insert.action_class("user")
class InsertUserActions:
    def vim_normal_mode():
        """
        Change vim to normal mode
        """
        actions.key("escape ` ^")
        # Can take vim a little to be ready for normal keys
        actions.sleep(0.1)


@ctx_insert.action_class("edit")
class InsertEditActions:
    def undo():
        actions.key("ctrl-o z")

    def redo():
        actions.key("ctrl-o shift-z")

    def paste():
        actions.key("ctrl-o V")

    def indent_more():
        actions.key("ctrl-o > >")

    def indent_less():
        actions.key("ctrl-o < <")

    def line_insert_down():
        actions.key("end enter")


@ctx_visual.action_class("user")
class VisualUserActions:
    pass


@ctx_visual.action_class("edit")
class VisualEditActions:
    pass


undo_checkpointer = None
def _register_undo_checkpointer(window):
    global undo_checkpointer

    def _undo_checkpointer():
        if window.title.startswith("VIM i"):
            actions.key("ctrl-g u")

    if undo_checkpointer is not None:
        cron.cancel(undo_checkpointer)

    if window.title.startswith("VIM"):
        undo_checkpointer = cron.interval(
            "1s",
            _undo_checkpointer
        )

# ui.register("win_focus", _register_undo_checkpointer)
