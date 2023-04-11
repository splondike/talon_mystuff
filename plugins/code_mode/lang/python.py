from talon import Context, actions


ctx = Context()

ctx = Context()
ctx.matches = """
tag: user.python
"""


ctx.lists["self.code_mode_lang_token"] = {
    "assign": "literal: = ",
    "equal to": "literal: == ",
    "colgap": "literal:: ",
    "if": "literal:if ",
    "else": "literal:else ",
    "else if": "literal:elif ",
    "has attribute": "literal:hasattr",
    "not": "literal:not ",
    "and": "literal:and ",
    "or": "literal:or ",
    "def": "def",
    "class": "class ",
    "from": "from ",
    "import": "import ",
    "date time": "datetime",
    "range": "range",
    "enumerate": "enumerate",
    "print": "print",
    "dict": "dict",
    "list": "list",
    "with": "with",
}
