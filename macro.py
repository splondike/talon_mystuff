from talon import Context, actions

ctx = Context()


@ctx.action_class("user")
class OverriddenActions:
    def noise_trigger_pop():
        actions.core.repeat_command(1)
