from talon import Context, actions

ctx = Context()
ctx.matches = """
app.exe: kitty
"""

ctx_no_vim = Context()
ctx_no_vim.matches = """
app.exe: kitty
and not title: /^VIM/
"""


@ctx_no_vim.action_class("edit")
class Actions:
    def paste():
        actions.key("ctrl-alt-v")
