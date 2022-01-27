from talon import Module, Context

mod = Module()
mod.list("mystuff_special_key", desc="extra special keys")
mod.list("mystuff_symbol_key", desc="extra symbol keys")

ctx = Context()
ctx.lists["user.special_key"] = {
    "rend": "end",
    "enter": "enter",
    "escape": "escape",
    "home": "home",
    "insert": "insert",
    "pagedown": "pagedown",
    "page down": "pagedown",
    "pageup": "pageup",
    "page up": "pageup",
    "space": "space",
    "tab": "tab",
    "junk": "backspace",
    "drill": "delete"
}
ctx.lists["user.mystuff_symbol_key"] = {
    "semi": ";",
}

@ctx.capture("user.symbol_key", rule="{user.symbol_key} | {user.mystuff_symbol_key}")
def symbol_key(m):
    return str(m)
