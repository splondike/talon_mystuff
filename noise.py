"""
Map noises (like pop) to actions so they can have contextually differing behavior
"""

import datetime

from talon import Module, Context, actions, noise, registry, cron

mod = Module()
ctx = Context()
ctx.matches = """
not mode: sleep
"""

# TODO: Make these settings
hiss_click_lower_bound = 500


hiss_click_timeout = None


@mod.action_class
class Actions:
    def noise_trigger_hiss(direction: bool):
        """
        Called when the user makes a 'hiss' noise. Listen to
        https://noise.talonvoice.com/static/previews/hiss.mp3 for an
        example.
        """
        global hiss_click_timeout

        def _trigger_hiss_click():
            global hiss_click_timeout
            actions.user.noise_trigger_hiss_click()
            hiss_click_timeout = None

        if direction:
            hiss_click_timeout = cron.after(
                f"{hiss_click_lower_bound}ms",
                _trigger_hiss_click
            )
        else:
            if hiss_click_timeout:
                cron.cancel(hiss_click_timeout)

    def noise_trigger_hiss_click():
        """
        Triggered when the user hisses for an appropriate length of time
        """
        actions.skip()


@ctx.action("user.noise_trigger_hiss_click")
def toggle_dense_grid():
    if "user.full_mouse_grid_showing" in registry.tags:
        actions.user.full_grid_close()
    else:
        actions.user.full_grid_activate()


def _hiss_trigger(x):
    actions.user.noise_trigger_hiss(x)


noise.register("hiss", _hiss_trigger)
