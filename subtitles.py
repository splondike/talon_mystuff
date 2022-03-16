"""
Show a small panel in my status tray containing the last utterance, current mode indicator, and time
since last utterance
"""

import math
import datetime
from talon import canvas, ui, speech_system, scope, cron


last_phrase = ""
last_phrase_time = None

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
    left = 150
    top = rect.height

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
    can.draw_text(label, left+2, top - 3)
    can.paint.color = "ffffff"
    can.draw_text(label, left, top - 5)

def post_phrase(phrase):
    global last_phrase, last_phrase_time

    last_phrase = " ".join(phrase["text"])
    last_phrase_time = datetime.datetime.now()
    can.freeze()

rect = ui.main_screen().rect
can = canvas.Canvas.from_rect(rect)
can.register("draw", draw)
can.freeze()

speech_system.register("post:phrase", post_phrase)
scope.register("main.mode", can.freeze)
cron.interval("10s", can.freeze)
