from talon import Module, Context, app

mod = Module()
ctx = Context()

mod.list("shopping_list_unit", desc="Units for shopping list items")

mod.list("shopping_list_word", desc="Words for ingredients")

shopping_list_word_list_path = mod.setting(
    "shopping_list_word_list_path",
    type=str,
    desc="Path to a file listing shopping list ingredient words"
)

ctx.lists["user.shopping_list_unit"] = {
    "gram": "g",
    "milli litre": "ml",
    "kilo gram": "kg",
}


@mod.capture(rule="<number> [point <number_small>] {user.shopping_list_unit}")
def shopping_list_quantity(m) -> str:
    return "".join(map(lambda x: "." if x == "point" else str(x), m)) + " "

@mod.capture(rule="({user.shopping_list_word})+")
def shopping_list_phrase(m) -> str:
    return " ".join(m)

def load_word_list():
    path = shopping_list_word_list_path.get()
    if not path:
        return

    with open(path) as fh:
        ctx.lists["user.shopping_list_word"] = {
            line.strip(): line.strip()
            for line in fh.readlines()
        }

app.register("ready", load_word_list)
