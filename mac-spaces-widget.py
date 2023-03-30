import json
import subprocess
from collections import Counter

from talon import canvas, screen, fs, cron, app
from talon.types import Rect

def calc_space_info():
    proc = subprocess.run(["/opt/homebrew/bin/yabai", "-m", "query", "--spaces"], capture_output=True)
    space_info = json.loads(proc.stdout)

    space_count = len(space_info)
    usage = Counter()
    for space in space_info:
        usage.update(space["windows"])

    rtn = []
    for space in space_info:
        has_private_window = any(usage[window_id] == 1 for window_id in space["windows"])
        if has_private_window or space["has-focus"]:
            rtn.append({
                "index": space["index"],
                "active": space["has-focus"]
            })

    return {
        "active_spaces": rtn,
        "space_count": space_count
    }


def draw(skcanvas):
    space_info = calc_space_info()
    skcanvas.draw_rect(skcanvas.rect)
    for i, space in enumerate(space_info["active_spaces"]):
        skcanvas.paint.color = "666666" if space["active"] else "333333"
        box_x = skcanvas.x + i * (cell_width + cell_padding)
        rect = Rect(
            box_x,
            skcanvas.y,
            cell_width,
            cell_height
        )
        skcanvas.draw_rect(rect)
        skcanvas.paint.color = "aaaaaa"
        label = str(space["index"])
        dims = skcanvas.paint.measure_text(label)[1]
        skcanvas.draw_text(
            label,
            box_x + (cell_width - dims.width) // 2 - dims.x,
            (cell_height - dims.height) // 2 - dims.y
        )


# if app.platform == "mac":
if False:
    space_info = calc_space_info()

    cell_width = 25
    cell_height = 25
    cell_padding = 1

    total_width = (cell_width + cell_padding) * space_info["space_count"]

    can = canvas.Canvas.from_rect(Rect(0, 0, total_width, cell_height))

    can.register("draw", draw)
    can.freeze()

    def reposition_canvas():
        main_screen = screen.main_screen()
        can.move(main_screen.width - 500 - total_width, 0)

    cron.interval("5s", reposition_canvas)
    reposition_canvas()

    fs.watch("/Users/stefansk/osx-scripts/misc/spaces-trigger", lambda _, _1: can.freeze())
