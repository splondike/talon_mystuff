"""
Map noises (like pop) to actions so they can have contextually differing behavior
"""

import datetime

from talon import Module, Context, actions, noise, registry

mod = Module()
ctx = Context()
ctx.matches = """
not mode: sleep
"""

# TODO: Make these settings
hiss_click_lower_bound = datetime.timedelta(milliseconds=500)
hiss_click_upper_bound = datetime.timedelta(milliseconds=2000)


last_hiss_down = None


@mod.action_class
class Actions:
    def noise_trigger_hiss(direction: bool):
        """
        Called when the user makes a 'hiss' noise. Listen to
        https://noise.talonvoice.com/static/previews/hiss.mp3 for an
        example.
        """
        global last_hiss_down

        now = datetime.datetime.now()

        if direction:
            last_hiss_down = now
        else:
            delta = (now - last_hiss_down)
            is_click = (
                (delta > hiss_click_lower_bound) and
                (delta < hiss_click_upper_bound)
            )
            if is_click:
                actions.user.noise_trigger_hiss_click()

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
