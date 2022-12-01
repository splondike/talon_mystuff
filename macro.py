from typing import List, Union

import os
import pathlib
import subprocess
import time

from talon import Module, Context, actions, ui, canvas, screen
from talon.types import Rect


mod = Module()
setting_talon_file = mod.setting(
    "macro_talon_file",
    type=str,
    desc="The file you want to keep your macros in",
    default=None
)

ctx = Context()

def get_full_macro_file_path():
    maybe_path = setting_talon_file.get()
    if maybe_path:
        return maybe_path
    else:
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../macros.talon"
        )


def update_file(filename, contents):
    with open(filename, "w") as fh:
        fh.write(contents)

    # So Talon will pick up the change
    pathlib.Path(filename).touch()


def append_lines(talonscript_lines: List[str], command: str = "macro play:"):
    """
    Appends the given talonscript lines to the bottom of the specified Talon command
    """

    talonscript_lines = ["    " + l for l in talonscript_lines]
    talonscript_lines += ["    #"]
    filename = get_full_macro_file_path()
    output_lines = []

    if os.path.exists(filename):
        with open(filename, "r") as fh:
            state = 0
            has_lines = False
            for line_ in fh.readlines():
                has_lines = True
                line = line_.rstrip()
                if state == 0:
                    output_lines.append(line)
                    if line.startswith(command):
                        state = 1
                elif state == 1:
                    if line.strip() == "":
                        output_lines += talonscript_lines
                        state = 2

                    output_lines.append(line)
                elif state == 2:
                    output_lines.append(line)

            if state == 0:
                if has_lines:
                    output_lines.append("")

                output_lines += [
                    command,
                ] + talonscript_lines
            elif state == 1:
                output_lines += talonscript_lines
    else:
        output_lines = [
            command,
        ] + talonscript_lines

    update_file(filename, "\n".join(output_lines))


def reset_macro(command: str = "macro play:"):
    filename = get_full_macro_file_path()
    output_lines = []

    if os.path.exists(filename):
        with open(filename, "r") as fh:
            state = 0
            for line_ in fh.readlines():
                line = line_.rstrip()
                if state == 0:
                    if line.startswith(command):
                        state = 1
                    else:
                        output_lines.append(line)
                elif state == 1:
                    if line == "":
                        state = 0

    update_file(filename, "\n".join(output_lines))


def mouse_helper_find_active_window_relative():
    """
    Builds a x/y tuple for the active window suitable for passing to
    the mouse_helper_move_active_window_relative action
    """

    rect = ui.active_window().rect
    return (
        str(actions.mouse_x() - rect.x),
        str(actions.mouse_y() - rect.y)
    )


@mod.action_class
class Actions:
    def macro_show_macro_file(action: str):
        """
        Opens up your macro_talon_file in your editor
        """

        if action == "edit":
            subprocess.Popen(["/home/normal/bin/mine/talon-macro-file", "edit", get_full_macro_file_path()])
        elif action == "view":
            subprocess.Popen(["/home/normal/bin/mine/talon-macro-file", "view", get_full_macro_file_path()])

    def macro_append_special_command(type: str, args: str=""):
        """
        Builds and adds the given command to the bottom of the default "custom macro play"
        """

        if type == "mouse jump relative":
            xpos, ypos = mouse_helper_find_active_window_relative()
            append_lines([
                f"user.mouse_helper_move_active_window_relative(\"{xpos}\", \"{ypos}\")",
                # Short sleep for convenience with hover or clicking delays
                "sleep(16ms)",
            ])
        elif type == "screen change":
            dimension = 10
            x = actions.mouse_x() - dimension//2
            y = actions.mouse_y() - dimension//2
            append_lines([f"user.macro_wait_region_change(\"{x} {y} {x+dimension} {y+dimension}\")"])

    def macro_wait_region_change(rect: Union[Rect, str], timeout: int=3):
        """
        Waits for the screen contents in the given rectangle to change. Raises an exception
        if timeout seconds have elapsed without the rectangle changing.

        If rectangle is a string then it is the same format as used by the relative rectangles
        in the talon_ui_helper package.
        """

        if type(rect) == str:
            # Don't actually support the full syntax yet, I'll probably move this action to the
            # talon_ui_helper package
            assert("-" not in rect)
            bits = [int(i) for i in rect.split(" ")]
            rect = Rect(bits[0], bits[1], bits[2] - bits[0], bits[3] - bits[0])

        # This is a bit of a gross way of doing comparison, but otherwise I think I have to
        # iterate the pixels myself
        curr_cap = screen.capture(rect.x, rect.y, rect.width, rect.height, retina=False).encode().data()
        for _ in range(timeout*10):
            new_cap = screen.capture(rect.x, rect.y, rect.width, rect.height, retina=False).encode().data()
            if new_cap != curr_cap:
                return
            time.sleep(0.1)

        raise RuntimeError(f"Timeout elapsed while waiting for change in {rect}")


@ctx.action_class("user")
class OverriddenActions:
    def pop():
        actions.core.repeat_command(1)
        
    def macro_record():
        reset_macro()
        actions.next()

    def macro_append_command(words: list[str]):
        if words[0] == "macro":
            return

        remaps = [
            ("touch", ["mouse_click(0)", "sleep(16ms)"]),
            ("righty", ["mouse_click(1)", "sleep(16ms)"]),
        ]

        command_str = " ".join(words)
        result = [f"mimic(\"{command_str}\")"]
        for needle, replacement in remaps:
            if command_str == needle:
                result = replacement

        append_lines(result)
