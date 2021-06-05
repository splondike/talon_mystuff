"""
Python code related to vim
"""

from talon import ui, actions, Context

ctx = Context()
ctx.matches = r"""
title: /^VIM/
"""

@ctx.action_class("win")
class VimWinActions:
    def file_ext():
        title = ui.active_window().title
        try:
            filename = title.split(" - ", 1)[1]
        except IndexError:
            # If file names get long, VIM seems to stop following
            # my title formatting rules
            return ""

        try:
            pos = filename.index(".")
            return filename[pos:]
        except ValueError:
            return ""

@ctx.action_class("user")
class VimUserActions:
    def pop():
        actions.key("ctrl-n")

    def paste(text: str):
        actions.insert(text)
