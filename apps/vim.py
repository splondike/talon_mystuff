"""
Python code related to vim
"""

from talon import ui, actions, Context

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
