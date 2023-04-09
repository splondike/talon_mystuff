"""
Python code related to vim
"""

from typing import Dict, Any, Optional, Tuple, List, Union
import re

from talon import actions, cron, ui, clip, Context, Module, speech_system

mod = Module()

ctx = Context()
ctx.matches = r"""
title: /^VIM/i
"""

mod.list("vim_text_object", desc="Text objects in vim")

ctx.lists["self.vim_text_object"] = {
    "word": "s w",
    "end": "$",
    "start": "^",
    "subscript": "s ]",
    "args": "s )",
    "brace": "s }",
    "angle": "s <",
    "outer angle": "a <",
    "string": "s '",
    "outer string": "a '",
    "dub string": "s \"",
    "outer dub string": "a \"",
    "item": "a a",
    "paragraph": "s p",
}


# Used internally in actions to save and restore the cursor position
INTERNAL_MARK = "z"


# We swap vim modes too quickly for Talon to keep track via the
# window title so within a phrase we track it manually ourselves
current_mode = None


def setup_mode(_):
    global current_mode
    title = actions.win.title()
    if title.startswith("VIM"):
        mode, _, _, _ = _parse_title_data()
        current_mode = mode
    else:
        current_mode = None


# TODO: Consider turning this off using a similar technique to disciples 2
# when we're not in Vim
speech_system.register("pre:phrase", setup_mode)


@mod.capture(
    rule="([abs] <digits>) | ([<digits>] [post] (<user.letter>+ | numb <user.number_key>+ | <user.symbol_key>) [(second|third|fourth)])"
)
def vim_jump_position(m) -> Dict[str, Any]:
    """
    Position we can jump to.

    <user.digits> is the line number with abs or abbreviation thereof otherwise,
    'post' is to say jump after the token,
    then the options in parentheses are:
        * the first letters or numbers of a word/token.
        * a symbol key
    second|third say to go to the second or third such match
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
    if "second" in m:
        repeated = 1
    elif "third" in m:
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
    # TODO: Add in a text object as an optional finisher or matcher here
    rule="""
        <digits> |
        (<digits> through <digits>) |
        (<digits> (<user.letter>+ | numb <user.number_key>+) [(second|third)])
    """
)
def vim_bring_range(m) -> Dict[str, Any]:
    """
    Range we can bring to the current cursor location

    <user.digits> is the line number (or abbreviation thereof),
    then the options in parentheses are:
        * the first letters or numbers of a word/token.
        * a symbol key
    """

    if len(m) == 1:
        return {
            "range_type": "line",
            "line": m.digits
        }
    elif len(m) == 3 and m[1] == "through":
        return {
            "range_type": "line_range",
            "line_start": m.digits_1,
            "line_end": m.digits_2
        }

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
    if "second" in m:
        repeated = 1
    elif "third" in m:
        repeated = 2

    return {
        "range_type": "token",
        "line": m.digits,
        "repeated": repeated,
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
        raise RuntimeError(f"Couldn't find line matching {uttered_line}")

    return closest


def _calculate_pos(
        text, target_type, target_chars,
        enable_iter=False, orig_col=0, repeated=0
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
                match.end()
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
    def vim_jump(target: Dict[str, Any]) -> int:
        """
        Jump to the given position
        """

        _, orig_line, orig_col, max_lines = _parse_title_data()
        actions.user.vim_set_mark(INTERNAL_MARK)

        if target["line"] != -1:
            target_line = _calculate_smart_line(
                target["line"],
                target["line_is_absolute"],
                orig_line,
                max_lines
            )
            is_same_line = target_line == orig_line
            if not is_same_line:
                actions.user.vim_go_line(target_line)
        else:
            is_same_line = True

        if target["target_type"] == "none":
            return -1

        with clip.capture() as cap:
            actions.user.vim_copy_line()

        line_text = cap.text()
        maybe_pos = _calculate_pos(
            line_text,
            target["target_type"],
            target["target_chars"],
            is_same_line,
            orig_col,
            repeated=target["repeated"]
        )

        if maybe_pos is None:
            return -1

        pos = maybe_pos[1] if target["is_post"] else maybe_pos[0]
        _, _, curr_col, _ = _parse_title_data()

        # <num>| uses screen columns, which doesn't work with wrap, hence
        # press the relevant arrow key n times to move. Jumping to the
        # start of the line first produces annoying flicker, so do this
        # calculation from the current cursor pos
        diff = pos - curr_col
        if diff < 0:
            actions.user.vim_escape_insert_keys(
                " ".join(str(abs(diff))) + " left"
            )
        elif diff > 0:
            actions.user.vim_escape_insert_keys(
                " ".join(str(abs(diff))) + " right"
            )
        else:
            pass

        return 0 if target["is_post"] else 1

    def vim_bring(target: Dict[str, Any]):
        """
        Bring the given range to the current cursor position
        """

        _, orig_line, orig_col, max_lines = _parse_title_data()
        calc_line = lambda line: _calculate_smart_line(line, False, orig_line, max_lines)

        if target["range_type"] == "line":
            target_line = calc_line(target["line"])
            actions.user.vim_set_mark(INTERNAL_MARK)
            if target_line != orig_line:
                actions.user.vim_go_line(target_line)
            actions.user.vim_copy_line()
            actions.user.vim_go_mark(INTERNAL_MARK)
            actions.user.vim_paste_after()
        elif target["range_type"] == "line_range":
            start_line = calc_line(target["line_start"])
            end_line = calc_line(target["line_end"])
            actions.user.vim_set_mark(INTERNAL_MARK)
            if start_line != orig_line:
                actions.user.vim_go_line(start_line)
            actions.user.vim_visual_line_mode()
            if end_line != start_line:
                actions.user.vim_go_line(end_line)
            actions.edit.copy()
            actions.user.vim_go_mark(INTERNAL_MARK)
            actions.user.vim_paste_after()
        elif target["range_type"] == "token":
            target_line = calc_line(target["line"])
            actions.user.vim_set_mark(INTERNAL_MARK)
            if target_line != orig_line:
                actions.user.vim_go_line(target_line)

            with clip.capture() as cap:
                actions.user.vim_copy_line()

            line_text = cap.text()
            maybe_pos = _calculate_pos(
                line_text,
                target["target_type"],
                target["target_chars"],
                enable_iter=True,
                repeated=target["repeated"]
            )
            if maybe_pos is None:
                actions.user.vim_go_mark(INTERNAL_MARK)
                return

            actions.user.vim_go_mark(INTERNAL_MARK)
            text = line_text[maybe_pos[0]-1:maybe_pos[1]]
            actions.user.vim_insert_mode()
            # This is just a bit more reliable than using the
            # clipboard
            actions.insert(text)

    def vim_visual_character_mode():
        """
        Change vim to visual character mode
        """
        global current_mode

        if current_mode == "n":
            actions.key("a")
        elif current_mode == "V":
            actions.key("escape a")
        elif current_mode == "i":
            # This little dance keeps the cursor position the same
            actions.key("escape ` ^")
            actions.key("a")

        current_mode = "v"

    def vim_visual_line_mode():
        """
        Change vim to visual line mode
        """
        global current_mode

        if current_mode == "n":
            actions.key("A")
        elif current_mode == "v":
            actions.key("escape A")
        elif current_mode == "i":
            # This little dance keeps the cursor position the same
            actions.key("escape ` ^")
            actions.key("A")

        current_mode = "V"

    def vim_set_mode(mode: str):
        """
        Changed vim to the indicated mode
        """
        global current_mode

        current_mode = mode

    def vim_normal_mode():
        """
        Change vim to normal mode
        """
        global current_mode

        if current_mode == "i":
            # This little dance keeps the cursor position the same
            actions.key("escape ` ^")
            # Can take vim a little to be ready for normal keys
            actions.sleep(0.1)
        elif current_mode in ("v", "V"):
            actions.key("escape")

        current_mode = "n"

    def vim_insert_mode(before_cursor: int = 1):
        """
        Change vim to insert mode. If before_cursor == 1 and in normal
        mode, then insert before the cursor, if == 0 then after,
        otherwise do nothing.
        """
        global current_mode

        if before_cursor not in (1, 0):
            return

        if current_mode == "i":
            return

        if current_mode in ("v", "V"):
            actions.key("escape")

        if before_cursor == 1:
            actions.key("s")
        else:
            actions.key("t")

        current_mode = "i"

    def vim_escape_insert_keys(key_blocks: Union[str, List[str]]):
        """
        Presses the given Talon key string blocks, potentially
        prefixing them with ctrl-o if we're in insert mode. Lets
        you avoid unnesessary mode switching.
        """

        if current_mode == "i":
            prefix = "ctrl-o "
        else:
            prefix = ""

        if isinstance(key_blocks, str):
            actions.key(prefix + key_blocks)
        else:
            for key_block in key_blocks:
                actions.key(prefix + key_block)


    def vim_go_line(line_number: int):
        """
        Goes to the specified line number
        """
        actions.user.vim_escape_insert_keys([" ".join(str(line_number) + "G")])

    def vim_copy_line():
        """
        Copies the current line to the vim default register
        """
        actions.user.vim_escape_insert_keys("C")

    def vim_set_mark(mark_name: str):
        """
        Sets a vim mark with the given name
        """
        actions.user.vim_escape_insert_keys("m " + mark_name)

    def vim_go_mark(mark_name: str):
        """
        Jump to the given mark
        """
        actions.user.vim_escape_insert_keys("` " + mark_name)

    def vim_paste_after():
        """
        Jump to the given mark
        """
        actions.user.vim_escape_insert_keys("V")


@ctx.action_class("edit")
class VimEditActions:
    def undo():
        actions.user.vim_escape_insert_keys("z")

    def redo():
        actions.user.vim_escape_insert_keys("shift-z")

    def copy():
        actions.user.vim_escape_insert_keys("c")

    def paste():
        actions.user.vim_escape_insert_keys("v")

    def indent_more():
        actions.user.vim_escape_insert_keys("> >")

    def indent_less():
        actions.user.vim_escape_insert_keys("< <")

    def find(text: str = None):
        actions.user.vim_normal_mode()
        actions.key("/")
        if text:
            actions.insert(text)
            actions.key("enter")

    def find_next():
        actions.user.vim_escape_insert_keys("ctrl-i")


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
