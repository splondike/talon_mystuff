import json
import subprocess
from talon import ui, canvas, screen, types, cron, app


def find_stack_positions():
    proc = subprocess.run(
        ["yabai", "-m" , "query", "--windows", "--space"],
        capture_output=True,
        check=True
    )
    result = json.loads(proc.stdout)

    stacked_windows = [
        window

        for window in result
        if window["is-visible"]
        # Teams has sise 0 windows on all spaces
        if window["frame"]["w"] > 0
        if window["stack-index"] != 0
    ]
    rtn = []
    while len(stacked_windows) > 0:
        first = stacked_windows.pop()
        ff = first["frame"]
        stack_count = 1

        new_windows = []
        for other in stacked_windows:
            of = other["frame"]
            same_stack = of["x"] == ff["x"] and of["y"] == ff["y"]
            if not same_stack:
                new_windows.append(other)
            else:
                stack_count += 1

        # stacked_windows = list(filter(matches, stacked_windows))
        stacked_windows = new_windows
        rtn.append({
            "stack_count": stack_count,
            **ff
        })

    return rtn


def draw(canvas):
    for pos in stack_positions:
        # canvas.draw_rect(types.Rect(pos["x"] + 5, pos["y"] + 5, 30, 20))
        label = str(pos["stack_count"])
        _, measurements = canvas.paint.measure_text(label)
        canvas.paint.color = "#000000"
        cx = pos["x"] + 15
        cy = pos["y"] + 15
        canvas.draw_circle(cx, cy, 10)
        canvas.paint.color = "#ffffff"
        canvas.draw_text(
            label,
            cx - measurements.width // 2 - measurements.x,
            cy - measurements.height // 2 - measurements.y
        )


if app.platform == "mac":
    stack_positions = []
    debounce_handle = None
    can = canvas.Canvas.from_screen(screen.main_screen())
    can.register("draw", draw)

    def refresh_positions():
        global debounce_handle
        def _inner():
            global stack_positions
            stack_positions = find_stack_positions()
            can.freeze()

        if debounce_handle:
            cron.cancel(debounce_handle)

        debounce_handle = cron.after("30ms", _inner)

    ui.register("win_move", lambda x: refresh_positions())
    ui.register("win_resize", lambda x: refresh_positions())
    ui.register("win_focus", lambda x: refresh_positions())
    refresh_positions()
