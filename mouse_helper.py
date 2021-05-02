import os
import subprocess

from talon import actions, clip, screen, Module
from talon.types import Rect as TalonRect
from talon.experimental import locate


mod = Module()


def find_active_window_rect() -> TalonRect:
    """
    The Talon active window rect detector is buggy under LInux. So allow getting it a
    different way.
    """

    active_window_id = subprocess.run(
        ["xdotool", "getactivewindow"],
        capture_output=True,
        check=True
    ).stdout.strip()
    active_window_geom = subprocess.run(
        ["xdotool", "getwindowgeometry", "--shell", active_window_id],
        capture_output=True,
        check=True
    ).stdout
    val_map = {
        key.decode("utf8"): int(val)
        for line in active_window_geom.splitlines()
        for key, val in (line.split(b"="),)
    }

    return TalonRect(
        val_map["X"],
        val_map["Y"],
        val_map["WIDTH"],
        val_map["HEIGHT"],
    )


def calculate_relative(modifier: str, start: int, end: int) -> int:
    """
    Helper method for settings. Lets you specify numbers relative to a
    range. For example:

        calculate_relative("-10", 0, 100) == 90
        calculate_relative("10", 0, 100) == 10
        calculate_relative("-0", 0, 100) == 100
    """
    if modifier.startswith("-"):
        modifier_ = int(modifier[1:])
        rel_end = True
    elif modifier == ".":
        # In the middle
        return (end + start) // 2
    else:
        modifier_ = int(modifier)
        rel_end = False

    if rel_end:
        return end - modifier_
    else:
        return start + modifier_


mouse_pos = None


@mod.action_class
class MouseActions:
    def mouse_pos_save():
        """
        Saves the mouse position to a global variable
        """

        global mouse_pos

        mouse_pos = (actions.mouse_x(), actions.mouse_y())

    def mouse_pos_restore():
        """
        Restores a saved mouse position
        """

        if mouse_pos is None:
            return

        actions.mouse_move(
            mouse_pos[0],
            mouse_pos[1]
        )

    def mouse_pos_active_window_relative(xpos: str, ypos: str):
        """
        Positions the mouse relative to the active window
        """

        rect = find_active_window_rect()

        actions.mouse_move(
            calculate_relative(xpos, 0, rect.width) + rect.x,
            calculate_relative(ypos, 0, rect.height) + rect.y,
        )

    def mouse_move_relative(xdelta: int, ydelta: int):
        """
        Moves the mouse relative to its current position
        """

        new_xpos = actions.mouse_x() + xdelta
        new_ypos = actions.mouse_y() + ydelta
        actions.mouse_move(new_xpos, new_ypos)

    def mouse_move_image_relative(icon_path: str, xdelta: int, ydelta: int, disambiguator: int=0):
        """
        Moves the mouse relative to the icon given in icon_path.

        :param icon_path: Path relative to this file to the icon to search for.
        :param xdelta: Amount to shift in the x direction relative to the
            center of the icon.
        :param ydelta: Amount to shift in the y direction relative to the
            center of the icon.
        :param disambiguator: If there are multiple matches, use this to indicate
            which one you want to match. Matches are ordered left to right top to
            bottom and this is just an index into that ordered list.
        """

        rect = find_active_window_rect()
        # img = screen.capture(rect.x, rect.y, rect.width, rect.height)
        matches = locate.locate(
            os.path.join(
                os.path.dirname(__file__),
                "icons",
                icon_path
            ),
            rect=rect
        )

        if len(matches) <= disambiguator:
            return

        sorted_matches = sorted(
            matches,
            key=lambda m: (m.x, m.y)
        )

        match_rect = sorted_matches[disambiguator]

        actions.mouse_move(
            round(rect.x + match_rect.x + (match_rect.width / 2) + xdelta),
            round(rect.y + match_rect.y + (match_rect.height / 2) + ydelta),
        )

    def copy_mouse_info():
        """
        Copies mouse information to the clipboard
        """

        rect = find_active_window_rect()
        xpos = actions.mouse_x() - rect.x
        xpos_inv = xpos - rect.width
        ypos = actions.mouse_y() - rect.y
        ypos_inv = ypos - rect.height

        clip.set_text(
            f"xpos: {xpos} {xpos_inv} ypos: {ypos} {ypos_inv}"
        )
