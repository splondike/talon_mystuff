from talon import Context, actions

ctx = Context()
ctx.matches = """
app.exe: kitty
"""

@ctx.action_class("edit")
class KittyActions:
    def line_start():
        actions.key("ctrl-a")

    def line_end():
        actions.key("ctrl-e")

    def word_left():
        actions.key("alt-b")

    def word_right():
        actions.key("alt-f")

    def delete_line():
        actions.edit.line_start()
        actions.key("ctrl-k")
