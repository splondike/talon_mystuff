"""
Scrappy voice UI for Battle for Wesnoth. Actions to let you
control the regular game UI using voice.
"""

import cv2
import numpy as np
from talon import canvas, ui, actions, Module
from talon.skia.typeface import Typeface

# Set up the game grid
def _draw_grid(canvas):
    global grid_positions
    paint = canvas.paint
    paint.textsize = 12
    paint.typeface = Typeface.from_name('monospace')
    paint.style = paint.Style.FILL
    paint.color = 'white'

    for text, (xpos, ypos) in grid_positions.items():
        canvas.draw_text(
            text,
            xpos,
            ypos
        )

screen = ui.screens()[0]
row = 100
col = int(screen.width) - 190

xlabels = "abcdefghijklmnopqrstuvwxyz!$%*+=-"
ylabels = list(map(str, range(1, 99)))
grid_positions = {}
for yidx, ypos in enumerate(range(row, int(screen.height), 72)):
    for xidx, xpos in enumerate(range(0, col, 54)):
        text = xlabels[xidx] + ylabels[yidx]
        grid_positions[text] = (xpos, ypos)

grid_interface = canvas.Canvas.from_screen(screen)
grid_interface.register("draw", _draw_grid)
grid_interface.freeze()
grid_interface.hide()

mod = Module()


@mod.action_class
class WesnothActions:
    def wesnoth_grid_show():
        """
        Show the grid overlay
        """
        grid_interface.show()

    def wesnoth_grid_hide():
        """
        Show the grid overlay
        """
        grid_interface.hide()

    def wesnoth_grid_mouse_move(anchor: str):
        """
        Show the grid overlay
        """
        global grid_positions

        maybe_coords = grid_positions.get(anchor)
        if maybe_coords:
            actions.mouse_move(
                maybe_coords[0],
                maybe_coords[1]
            )


# Hide the grid when we swap off the application
ui.register("win_focus", lambda _: WesnothActions.wesnoth_grid_hide())
