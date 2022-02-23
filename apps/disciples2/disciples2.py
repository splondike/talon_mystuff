from typing import Tuple


from talon import actions, ui, cron, settings, ctrl, Context, Module

mod = Module()
mod.apps.disciples2 = """
title: Disciples II
"""

setting_poll_screen = mod.setting(
    "disciples2_poll_screen",
    type=int,
    desc="Used to activate and deactivate the poller that populates the disciples ii screen scope",
    default=0
)


@mod.scope
def disciples_screen_scope():
    if ui.active_window().title != "Disciples II":
        return {}

    # Put these in order of likelihood so we can short circuit the checks
    patches = [
        ("-92 0 -66 17", "e60fb4ee7f877058f49e", "world"),
        ("391 -52 -389 -34", "b4f15a9c055984b96155", "combat"),
        ("-92 0 -67 18", "d4ae30a227592155d9b0", "capital"),
        ("-190 -97 -163 -58", "331fdee083dd1691434e", "build"),
        ("-16 247 -1 281", "8e895e0105d4592f6acc", "city"),
        ("0 0 24 25", "b99fa391029c5e843619", "options"),
        ("-245 122 -220 150", "0a4d885cdf08f28f2d3d", "loadgame"),
        ("-99 0 -73 23", "099af210dfc7a9a42296", "title"),
        ("-99 0 -73 23", "81660e02f82037ed68f1", "title"),
    ]

    for relative_rectangle, hash, result in patches:
        rect = actions.user.mouse_helper_calculate_relative_rect(relative_rectangle, "active_window")
        curr_hash = actions.user.mouse_helper_calculate_rectangle_hash(rect)
        if curr_hash == hash:
            print(result)
            return {
                "disciples2_screen": result
            }

    print("unknown")
    return {
        "disciples2_screen": "unknown"
    }


screen_poller_job = None
def toggle_screen_poller(setting_value):
    global screen_poller_job
    if setting_value == 1:
        if screen_poller_job is None:
            screen_poller_job = cron.interval("1s", disciples_screen_scope.update)
    elif screen_poller_job is not None:
        cron.cancel(screen_poller_job)
        screen_poller_job = None

settings.register("user.disciples2_poll_screen", toggle_screen_poller)

@mod.capture(rule="[big] (left | right | up | down)")
def disciples2_map_move(m) -> Tuple[int, int]:
    print(m)
    step = 10 if len(m) == 1 else 20

    cx = 719
    cy = 128

    result = {
        "left": (cx - step, cy),
        "right": (cx + step, cy),
        "up": (cx, cy - step),
        "down": (cx, cy + step),
    }[m[-1]]
    return (str(result[0]), str(result[1]))


@mod.action_class
class Actions:
    def disciples2_unit_select(unit: int):
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

    def disciples2_parse_screen():
        """
        Test
        """
        import time
        for y in range(0, 400, 20):
            for x in range(0, 400, 20):
                actions.mouse_move(x + 10, y + 10)
                ctrl.mouse_click(button=1, down=True)
                time.sleep(0.05)
                ctrl.mouse_click(button=1, up=True)
                time.sleep(0.05)
