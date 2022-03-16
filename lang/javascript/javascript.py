from talon import Module, Context, actions, settings

mod = Module()
ctx = Context()
ctx.matches = """
mode: user.typescript
mode: command
and code.language: typescript
"""

@ctx.action_class("user")
class UserActions:
    def code_operator_equal():
        actions.auto_insert(" === ")

    def code_operator_not_equal():
        actions.auto_insert(" !== ")
