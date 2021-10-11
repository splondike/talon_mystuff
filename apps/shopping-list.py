from talon import Module, Context

mod = Module()
ctx = Context()

mod.list("shopping_list_unit", desc="Units for shopping list items")

ctx.lists["user.shopping_list_unit"] = {
    "gram": "g",
    "milli litre": "ml",
    "kilo gram": "kg",
}


@mod.capture(rule="<number> [point <number_small>] {user.shopping_list_unit}")
def shopping_list_quantity(m) -> str:
    return "".join(map(lambda x: "." if x == "point" else str(x), m)) + " "

