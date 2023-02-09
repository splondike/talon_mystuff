from talon import Context, ctrl

ctx_linux = Context()
ctx_linux.matches = """
os: linux
"""

ctx_mac = Context()
ctx_mac.matches = """
os: mac
"""

@ctx_linux.action("mouse_scroll")
def mouse_scroll(y: float=0, x: float=0, by_lines: bool=True):
    ctrl.mouse_scroll(y=y, x=x, by_lines=by_lines)


@ctx_mac.action("mouse_scroll")
def mouse_scroll(y: float=0, x: float=0, by_lines: bool=False):
    # Quick hack to make it so I don't have to alter all my Linux numbers
    ctrl.mouse_scroll(y=y * -50, x=x, by_lines=by_lines)
