from talon import Module, Context

mod = Module()
mod.list("mystuff_special_key", desc="extra special keys")
mod.list("mystuff_symbol_key", desc="extra symbol keys")

ctx = Context()
ctx.lists["user.mystuff_special_key"] = {
    "enta": "enter",
}
ctx.lists["user.mystuff_symbol_key"] = {
    "semi": ";",
}

@ctx.capture("user.special_key", rule="{user.special_key} | {user.mystuff_special_key}")
def special_key(m):
    return str(m)

@ctx.capture("user.symbol_key", rule="{user.symbol_key} | {user.mystuff_symbol_key}")
def symbol_key(m):
    return str(m)
