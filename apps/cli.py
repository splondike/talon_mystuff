from talon import Context, actions

ctx = Context()
ctx.matches = "app.exe: kitty"

@ctx.action_class("edit")
class Actions:
    def paste():
        actions.key("ctrl-alt-v")