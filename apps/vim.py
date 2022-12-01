"""
Python code related to vim
"""

from talon import ui, actions, cron, ui, Context, Module

mod = Module()

ctx = Context()
ctx.matches = r"""
title: /^VIM/
"""

ctx_normal = Context()
ctx_normal.matches = r"""
title: /^VIM n/
"""

ctx_insert = Context()
ctx_insert.matches = r"""
title: /^VIM i/
"""

@mod.action_class
class VimActions:
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

    def vim_normal_mode():
        """
        Change vim to normal mode
        """

        # Do nothing, and trick Talon into not complaining
        a = 1


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
class VimUserActions:
    def pop():
        actions.key("ctrl-n")

    def paste(text: str):
        actions.insert(text)

    def vim_normal_mode():
        actions.key("escape")
        # Can take vim a little to be ready for normal keys
        actions.sleep(0.1)


@ctx_insert.action_class("edit")
class InsertModeEditActions:
    def undo():
        actions.key("ctrl-o z")

    def redo():
        actions.key("ctrl-o shift-z")

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

@ctx_normal.action_class("edit")
class NormalModeEditActions:
    def undo():
        actions.key("z")
    
    def redo():
        actions.key("shift-z")

    def indent_more():
        actions.insert(">>")
    
    def indent_less():
        actions.insert("<<")

# ui.register("win_focus", _register_undo_checkpointer)
