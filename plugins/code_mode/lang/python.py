from talon import Context, actions


ctx = Context()

ctx = Context()
ctx.matches = """
tag: user.python
"""


ctx.lists["self.code_mode_lang_token"] = {
    "assign": "literal: = ",
    "at sign": "literal:@",
    "equal to": "literal: == ",
    "colgap": "literal:: ",
    "colon": "literal::",
    "if": "literal:if ",
    "for": "literal:for ",
    "in": "literal: in ",
    "else": "literal:else ",
    "else if": "literal:elif ",
    "has attribute": "literal:hasattr",
    "negate": "literal:not ",
    "and": "literal:and ",
    "or": "literal:or ",
    "def": "literal:def ",
    "class": "literal:class ",
    "from": "literal:from ",
    "import": "literal:import ",
    "date time": "literal:datetime",
    "range": "literal:range",
    "enumerate": "literal:enumerate",
    "print": "literal:print",
    "dict": "literal:dict",
    "list": "literal:list",
    "with": "literal:with ",
}
