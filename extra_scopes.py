import subprocess
from talon import Module, ui


mod = Module()


def get_active_window_role():
    """
    Determine the X11 role of the currently active window
    """

    process_result = subprocess.run(
        ["xprop", "-id", str(ui.active_window().id)],
        check=True,
        capture_output=True
    ).stdout
    for line in process_result.decode().splitlines():
        if line.startswith("WM_WINDOW_ROLE"):
            return line.split(" = \"")[1][:-1]

    return "unknown"


@mod.scope
def window_role_scope():
    return {
        "window_role": get_active_window_role()
    }


ui.register("win_focus", lambda _: window_role_scope.update())