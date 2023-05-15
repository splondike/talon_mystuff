"""
Python code related to vim
"""

from typing import Dict, Any, Optional, Tuple, List, Union
import re
import subprocess

from talon import actions, ui, clip, Context, Module

mod = Module()

ctx = Context()
ctx.matches = r"""
title: /^VIM/i
"""

mod.list("vim_text_object", desc="Text objects in vim")

ctx.lists["self.vim_text_object"] = {
    "word": "sw",
    "sub word": "si",
    "end": "$",
    "start": "^",
    "subscript": "s]",
    "paren": "s)",
    "brace": "s}",
    "angle": "s<",
    "outer angle": "a<",
    "string": "s'",
    "outer string": "a'",
    "quad": "s\"",
    "outer quad": "a\"",
    "item": "aa",
    "paragraph": "sp",
    "outer paragraph": "tp",
}

# Used internally in actions to save and restore the cursor position
INTERNAL_MARK = "z"

# TODO: Use the RPC for all key presses, and use them unmapped where possible to make this code
# workregardless of people's custom config. Could probably also remove the
# key_wait setting then


@mod.capture(
    rule="([abs] <digits>) | ([[abs] <digits>] [post] (<user.letter>+ | numb <user.number_key>+ | <user.symbol_key>) [(second|third|fourth)])"
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


@mod.capture(rule="<digits> | (<digits> past <digits>)")
def vim_line_range(m) -> Dict[str, Any]:
    """
    Capture a range of one or more lines
    """

    return {
        "start_line": m.digits_1,
        "end_line": m.digits_2 if hasattr(m, "digits_2") else None
    }


@mod.capture(
    # TODO: Add in a text object as an optional finisher or matcher here
    rule="""
        <digits> |
        (<digits> past <digits>) |
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
    elif len(m) == 3 and m[1] == "past":
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


def _calculate_smart_line(uttered_line, is_absolute, curr_line, max_lines) -> int:
    if is_absolute or uttered_line >= 100:
        return uttered_line

    curr_hundreds = 100 * (curr_line // 100)
    curr_rest = curr_line % 100

    if curr_rest == uttered_line:
        # We just said the current line
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
        enable_iter=False, orig_col=0, repeated=0,
        search_forward=True
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
    if search_forward:
        for i, (start, _) in enumerate(spans):
            if not enable_iter or orig_col < start:
                matching_idx = i
                break
    else:
        for i, (start, _) in reversed(list(enumerate(spans))):
            if not enable_iter or orig_col > start:
                matching_idx = i
                break

    return spans[matching_idx + repeated % len(spans)]


def _fetch_buffer_dimensions() -> Tuple[int, int, int]:
    """
    Return the current line, column position, and max lines for
    the current buffer
    """
    bits = actions.user.vim_call_rpc_function(
        "join([line('.'), col('.'), line('$')], ' ')"
    ).split(' ')
    return tuple(map(int, bits))


@mod.action_class
class VimActions:
    def vim_jump(target: Dict[str, Any], search_forward: int = 1) -> int:
        """
        Jump to the given position
        """

        orig_line, orig_col, max_lines = _fetch_buffer_dimensions()
        # For use with 'pull'
        actions.user.vim_set_mark(INTERNAL_MARK)

        if target["line"] != -1:
            target_line = _calculate_smart_line(
                target["line"],
                target["line_is_absolute"],
                orig_line,
                max_lines
            )
            is_same_line = target_line == orig_line
        else:
            is_same_line = True
            target_line = orig_line

        if target["target_type"] == "none":
            actions.user.vim_move_cursor(target_line)
            return -1

        line_text = actions.user.vim_get_line(
            target_line
        )
        maybe_pos = _calculate_pos(
            line_text,
            target["target_type"],
            target["target_chars"],
            is_same_line,
            orig_col,
            repeated=target["repeated"],
            search_forward=search_forward == 1
        )

        if maybe_pos is None:
            return -1

        pos = maybe_pos[1] if target["is_post"] else maybe_pos[0]
        actions.user.vim_move_cursor(target_line, pos)

        return 0 if target["is_post"] else 1

    def vim_take_line_range(target: Dict[str, Any]):
        """
        Enter visual line mode and select the given range of lines
        """

        orig_line, orig_col, max_lines = _fetch_buffer_dimensions()
        calc_line = lambda line: _calculate_smart_line(line, False, orig_line, max_lines)

        actions.user.vim_go_line(calc_line(target["start_line"]))
        actions.user.vim_visual_line_mode()
        if "end_line" in target:
            actions.user.vim_go_line(calc_line(target["end_line"]))

    def vim_bring(target: Dict[str, Any]):
        """
        Bring the given range to the current cursor position
        """

        orig_line, orig_col, max_lines = _fetch_buffer_dimensions()
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
        current_mode = actions.user.vim_get_mode()

        if current_mode == "n":
            actions.key("a")
        elif current_mode == "V":
            actions.key("escape a")
        elif current_mode == "i":
            # This little dance keeps the cursor position the same
            actions.key("escape ` ^")
            actions.key("a")

    def vim_visual_line_mode():
        """
        Change vim to visual line mode
        """
        current_mode = actions.user.vim_get_mode()

        if current_mode == "n":
            actions.user.vim_call_rpc_function("V", "normal!")
        elif current_mode in ("v", "V"):
            # Don't know how to go to normal mode using call_rpc here
            actions.user.vim_send_rpc_keys("<Esc>")
            actions.user.vim_call_rpc_function("V", "normal!")
        elif current_mode == "i":
            actions.user.vim_call_rpc_function("stopinsert", "command")
            actions.user.vim_call_rpc_function("V", "normal!")

    def vim_get_mode() -> str:
        """
        Get the current vim mode, one of 'n', 'i', 'v', 'V'
        """

        return actions.user.vim_call_rpc_function("mode()")

    def vim_normal_mode():
        """
        Change vim to normal mode
        """
        current_mode = actions.user.vim_get_mode()


        if current_mode == "i":
            # This little dance keeps the cursor position the same
            actions.key("escape ` ^")
            # Can take vim a little to be ready for normal keys
            actions.sleep(0.1)
        elif current_mode in ("v", "V"):
            actions.key("escape")

    def vim_insert_mode(before_cursor: int = 1):
        """
        Change vim to insert mode. If before_cursor == 1 and in normal
        mode, then insert before the cursor, if == 0 then after,
        otherwise do nothing.
        """
        current_mode = actions.user.vim_get_mode()

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

    def vim_escape_insert_keys(key_blocks: Union[str, List[str]]):
        """
        Presses the given Talon key string blocks, potentially
        prefixing them with ctrl-o if we're in insert mode. Lets
        you avoid unnesessary mode switching.
        """
        current_mode = actions.user.vim_get_mode()

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
        actions.user.vim_call_rpc_function(f"{line_number}G", "normal!")

    def vim_send_rpc_keys(keys: str):
        """
        Sends the given Vim-style key presses to Neovim. Prefer using
        vim_call_rpc_function
        """

        title = actions.win.title()
        if not title.startswith("VIM"):
            raise RuntimeError("Called when VIM not focussed")

        _, rpc_socket = title.split(" | ")

        subprocess.run(
            ["nvim", "--headless", "--server", rpc_socket, "--remote-send", keys],
            capture_output=True,
            check=True
        )

    def vim_call_rpc_function(command: str, mode: str="expression") -> str:
        """
        Runs the given Neovim expression on the given Neovim socket and
        returns the result as a string
        """

        title = actions.win.title()
        if not title.startswith("VIM"):
            raise RuntimeError("Called when VIM not focussed")

        _, rpc_socket = title.split(" | ")

        escaped_command = command.replace("\\", "\\\\").replace("\"", "\\\"")

        # See ':h function-list'
        # First send a harmless keypress in order to clear any operator pending
        # or repeat pending. The latter (e.g. pressing the 9 key) actually
        # causes the following remote-expr called to hang otherwise.
        subprocess.run(
            ["nvim", "--headless", "--server", rpc_socket, "--remote-send", "<F4>"],
            capture_output=True,
            check=True
        )
        if mode == "expression":
            expression = command
        elif mode == "normal":
            expression = f"execute(\"normal {escaped_command}\")"
        elif mode == "normal!":
            expression = f"execute(\"normal! {escaped_command}\")"
        elif mode == "command":
            expression = f"execute(\"{escaped_command}\")"
        else:
            raise RuntimeError(f"Unsupported mode {mode}")
        result = subprocess.run(
            ["nvim", "--headless", "--server", rpc_socket, "--remote-expr", expression],
            capture_output=True,
            check=True
        )
        return result.stderr.decode()

    def vim_get_line(line_number: int) -> str:
        """
        Grabs the given line number from the current buffer
        """

        escaped_result = actions.user.vim_call_rpc_function(f"getline({line_number})")
        return escaped_result.replace("^I", "\t")

    def vim_move_cursor(line_number: int, column_number: int = 1) -> str:
        """
        Grabs the given line number from the current buffer
        """
        return actions.user.vim_call_rpc_function(f"cursor({line_number}, {column_number})")

    def vim_copy_line():
        """
        Copies the current line to the vim default register
        """
        actions.user.vim_escape_insert_keys("C")

    def vim_set_mark(mark_name: str):
        """
        Sets a vim mark with the given name
        """
        actions.user.vim_call_rpc_function("m " + mark_name, "normal!")

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
        actions.user.vim_call_rpc_function("u", "normal!")

    def redo():
        actions.user.vim_call_rpc_function("Z", "normal")

    def copy():
        actions.user.vim_call_rpc_function("y", "normal!")

    def paste():
        actions.user.vim_call_rpc_function("p", "normal!")

    def indent_more():
        actions.user.vim_call_rpc_function("> >", "normal")

    def indent_less():
        actions.user.vim_call_rpc_function("< <", "normal")

    def find(text: str = None):
        actions.user.vim_normal_mode()
        actions.key("/")
        if text:
            actions.insert(text)
            actions.key("enter")

    def find_next():
        actions.user.vim_escape_insert_keys("ctrl-i")

    def line_start():
        actions.user.vim_call_rpc_function("^", "normal!")

    def line_end():
        actions.user.vim_call_rpc_function("$", "normal!")
        actions.user.vim_send_rpc_keys("<Right>")


@ctx.action_class("win")
class VimWinActions:
    def file_ext():
        title = ui.active_window().title
        if not title.startswith("VIM"):
            # For some reason this gets called one final time
            # when swapping off the window
            return ""

        filename = title[4:title.find(" | ")]

        try:
            pos = filename.index(".")
            return filename[pos:]
        except ValueError:
            return ""
