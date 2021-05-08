from talon import Context, actions, settings

ctx = Context()
ctx.matches = "os: linux"

@ctx.action_class("user")
class Actions:
    def i3wm_launch():
        """Trigger the i3 launcher: ex rofi"""
        key = settings.get("user.i3_mod_key")
        actions.key(f"{key}-p")
