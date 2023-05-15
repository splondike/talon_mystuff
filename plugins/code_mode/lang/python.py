from talon import Context, actions


ctx = Context()

ctx = Context()
ctx.matches = """
tag: user.python
"""

python_tokens = {
    "assign": "literal: = ",
    "at sign": "literal:@",
    "equal to": "literal: == ",
    "not equal to": "literal: != ",
    "colgap": "literal:: ",
    "colon": "literal::",
    "if": "literal:if ",
    "self": "literal:self",
    "for": "literal:for ",
    "in": "literal: in ",
    "in": "literal: is ",
    "none": "literal:None",
    "true": "literal:True",
    "false": "literal:False",
    "else": "literal:else ",
    "else if": "literal:elif ",
    "has attribute": "literal:hasattr",
    "negate": "literal:not ",
    "and": "literal:and ",
    "or": "literal:or ",
    "def": "literal:def ",
    "class": "literal:class ;;formatter:PUBLIC_CAMEL_CASE",
    "from": "literal:from ",
    "import": "literal:import ",
    "range": "literal:range",
    "enumerate": "literal:enumerate",
    "print": "literal:print",
    "dict": "literal:dict",
    "list": "literal:list",
    "with": "literal:with ",
    "async": "literal:async ",
    "assert": "literal:assert ",
    "return": "literal:return ",
}
ctx.lists["self.code_mode_lang_token"] = python_tokens


@ctx.action_class("user")
class Actions:
    def code_mode_used_tokens():
        return actions.next() | set(python_tokens.keys())
