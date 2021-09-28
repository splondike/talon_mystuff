from talon import Context, ctrl

ctx = Context()
ctx.matches = """
os: linux
"""

@ctx.action("mouse_scroll")
def mouse_scroll(y: float=0, x: float=0, by_lines: bool=True):
    ctrl.mouse_scroll(y=y, x=x, by_lines=by_lines)
