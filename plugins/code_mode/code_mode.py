from typing import List, Set

from talon import Module, Context, actions

mod = Module()
mod.list("code_mode_project_token", desc="Project specific tokens")
mod.list("code_mode_seed_tokens", desc="User custom words that are always available")
mod.list("code_mode_lang_token", desc="Programming language specific tokens")
mod.list("code_mode_global_token", desc="Globally applicable tokens")

mod.tag("code_mode_active", desc="Activate the stack command")

ctx = Context()

ctx = Context()
global_tokens = {
    "dot": "literal:.",
    "equals": "literal:=",
    "spamma": "literal:, ",
    "space": "literal: ",
    "newline": "literal:\n",
    "args": "wrap:(,)",
    "angle": "wrap:<,>",
    "square": "wrap:[,]",
    "brace": "wrap:{,}",
    "quad": "wrap:\",\"",
    "string": "wrap:','",
    "hammer": "formatter:PUBLIC_CAMEL_CASE",
    "smash": "formatter:NO_SPACES",
    "title": "formatter:CAPITALIZE_ALL_WORDS",
    "snake": "formatter:SNAKE_CASE",
    "camel": "formatter:PRIVATE_CAMEL_CASE",
    "over": "control:out",
}
ctx.lists["self.code_mode_global_token"] = global_tokens


@mod.capture(rule="{self.code_mode_project_token}")
def code_mode_project_token(m) -> List[str]:
    """
    Intended for project specific tokens
    """
    return m.code_mode_project_token


@mod.capture(rule="{self.code_mode_seed_tokens}")
def code_mode_seed_tokens(m) -> List[str]:
    """
    Intended for generic words that are always available
    """
    return m.code_mode_seed_tokens


@mod.capture(rule="{self.code_mode_lang_token}")
def code_mode_lang_token(m) -> List[str]:
    """
    Intended for programming language specific tokens
    """
    return m.code_mode_lang_token


@mod.capture(rule="{self.code_mode_global_token}")
def code_mode_global_token(m) -> List[str]:
    """
    Default tokens that are always available
    """
    return m.code_mode_global_token

@mod.capture(
    # Ordering of captures is important in case project tokens
    # interfere with higher level ones
    rule="""(
        <self.code_mode_global_token> |
        <self.code_mode_lang_token> |
        <self.code_mode_seed_tokens> |
        <self.code_mode_project_token>
    )+"""
)
def code_mode_command(m) -> List[str]:
    return list(m)


@mod.action_class
class Actions:
    def code_mode_insert(command: List[str]):
        """
        Insert the given command
        """
        rtn = ""
        suffixes = []
        words = []
        default_formatter = "SNAKE_CASE"
        formatter = default_formatter

        def _flush_words():
            nonlocal rtn, formatter, words
            if len(words) > 0:
                rtn += actions.user.formatted_text(
                    " ".join(words),
                    formatter
                )
            formatter = default_formatter
            words = []

        command_items = [
            item
            for command_entry in command
            for item in command_entry.split(";;")
        ]
        for item in command_items:
            if item.startswith("literal:"):
                _flush_words()
                rtn += item[item.find(":") + 1:]
            elif item.startswith("wrap:"):
                _flush_words()
                left, right = item[item.find(":") + 1:].split(",")
                rtn += left
                suffixes.append(right)
            elif item.startswith("formatter:"):
                _flush_words()
                formatter = item[item.find(":") + 1:]
            elif item == "control:out":
                _flush_words()
                if len(suffixes) > 0:
                    rtn += suffixes.pop()
            else:
                words.append(item)

        _flush_words()
        suffix = ""
        if len(suffixes) > 0:
            suffix = "".join(reversed(suffixes))

        actions.insert(rtn + suffix)
        for _ in range(len(suffix)):
            actions.edit.left()

    def code_mode_used_tokens() -> Set[str]:
        """
        Lists out tokens that have already been mapped, Talon doesn't
        have defined semantics for which captures should override others.
        """

        return set(global_tokens.keys())

