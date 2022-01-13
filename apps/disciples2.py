from talon import actions, Context, Module

mod = Module()

ctx = Context()
ctx.matches = r"""
title: Disciples II
"""

@ctx.action_class("user")
class UserActions:
    def pop():
        actions.mouse_click(0)


@mod.action_class
class Actions:
    def disciples_unit_select(unit: int):
        """
        Moves the mouse to the given unit in the combat window
        """

        if unit > 6:
            return

        xdelta = [-114, -34][(unit - 1) % 2]
        ydelta = [-270, -160, -49][(unit - 1) // 2]

        actions.user.mouse_helper_move_image_relative(
            "2022-01-02_14.26.58.941328.png",
            0,
            xdelta,
            ydelta
        )
