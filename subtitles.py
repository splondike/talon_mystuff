"""
Show a small panel in my status tray containing the last utterance, current mode indicator, and time
since last utterance
"""

import math
import datetime
from talon import Module, canvas, ui, speech_system, scope, cron, app
from talon.types import Rect as TalonRect


last_phrase = ""
last_phrase_time = None
mod = Module()
can = None

setting_subtitle_placement = mod.setting(
    "subtitle_placement",
    type="str",
    default="0 0",
    desc="Where to put the subtitles"
)

def calculate_last_phrase_time():
    if last_phrase_time is None:
        return ""

    delta = (datetime.datetime.now() - last_phrase_time).total_seconds()
    opts = [("h", 3600), ("m", 60), ("s", 1)]
    for marker, divisor in opts:
        if delta >= divisor:
            return f"{math.floor(delta / divisor)}{marker}".rjust(3, " ")

    return " 1s"

def draw(can):
    mode_set = (scope.get("mode") or [])
    if "dictation" in mode_set:
        mode = "DM"
    elif "sleep" in mode_set:
        mode = "SM"
    else:
        mode = "CM"
    time = calculate_last_phrase_time()
    label = f"{mode} {time} {last_phrase}"

    can.paint.typeface = "monospace"
    can.paint.color = "000000"
    can.clear("000000")
    can.paint.color = "ffffff"
    top = can.rect.top + can.rect.height
    can.draw_text(label, can.rect.left, top - 5)

def post_phrase(phrase):
    global last_phrase, last_phrase_time, can

    last_phrase = " ".join(phrase["text"])
    last_phrase_time = datetime.datetime.now()
    can.freeze()

def calculate_relative(modifier: str, start: float, end: float) -> float:
    """
    Helper method for settings. Lets you specify numbers relative to a
    range. For example:

        calculate_relative("-10.0", 0, 100) == 90
        calculate_relative("10", 0, 100) == 10
        calculate_relative("-0", 0, 100) == 100

    Note that positions and offset are floats.
    """
    if modifier.startswith("-"):
        modifier_ = float(modifier[1:])
        rel_end = True
    elif modifier == ".":
        # In the middle
        return (end + start) // 2
    else:
        modifier_ = float(modifier)
        rel_end = False

    if rel_end:
        return end - modifier_
    else:
        return start + modifier_

def calculate_rect(rect, modifiers):
    x_mod, y_mod = modifiers.split(" ")
    width = 400
    height = 20
    return TalonRect(
        calculate_relative(x_mod, rect.x, rect.x + rect.width - width),
        calculate_relative(y_mod, rect.y, rect.y + rect.height - height),
        width,
        height
    )

def _ready():
    global can

    screen_rect = ui.main_screen().rect
    rect = calculate_rect(screen_rect, setting_subtitle_placement.get())
    can = canvas.Canvas.from_rect(rect)
    can.register("draw", draw)
    can.freeze()

    speech_system.register("post:phrase", post_phrase)
    scope.register("main.mode", can.freeze)
    cron.interval("10s", can.freeze)

app.register("ready", _ready)
