"""
Python code related to vim
"""

from talon import ui, actions, Context

ctx = Context()
ctx.matches = r"""
title: /VIM$/
"""

@ctx.action_class("win")
class VimWinActions:
    def file_ext():
        title = ui.active_window().title
        if "(" in title:
            bit, *_ = title.split("(")
            if bit.endswith(" + "):
                filename = bit[:-3]
            else:
                filename = bit[:-1]
        elif "..." in title:
            filename = title[:title.find("...")]
        else:
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
