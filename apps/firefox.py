from talon import Context, actions

ctx = Context()
ctx.matches = """
app: firefox
"""


@ctx.action_class("app")
class Actions:
    def tab_next():
        actions.key("ctrl-pagedown")

    def tab_previous():
        actions.key("ctrl-pageup")
