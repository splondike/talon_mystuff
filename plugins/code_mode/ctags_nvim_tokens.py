"""
Populates the code mode project tokens from a ctags file. Generate
the latter using ctags -R --kinds-all=*
"""

import os
import re

from talon import actions, ui, Context

ctx = Context()
ctx.matches = r"""
title: /^VIM/i
"""


last_working_dir = None
uppercase_letter = re.compile(r"([A-Z])")


def split_token(token):
    # Drop leading and trailing symbols
    token = token.strip("_$&*[]0123456789")

    # If underscore in word, split by underscore then recurse
    if "_" in token:
        rtn = []
        for subtoken in token.split("_"):
            rtn += split_token(subtoken)
        return rtn

    rtn = []
    buffer = ""
    for subtoken in uppercase_letter.split(token):
        if len(subtoken) == 1 and uppercase_letter.match(subtoken):
            buffer = subtoken.lower()
        elif subtoken != "":
            item = buffer + subtoken
            if len(item) > 1:
                rtn.append(item)
            buffer = ""

    return rtn


# tokens = ["hello_world", "_hello_world", "helloWorld", "HelloWorld", "Hello", "USBDrive", "_"]
# for token in tokens:
#     print(token, "->", split_token(token))


def update_list(window):
    global last_working_dir

    if not window.title.startswith("VIM"):
        return

    working_dir = actions.user.vim_call_rpc_function("$PWD")
    if working_dir == last_working_dir:
        # Don't update the list unless we need to
        return
    last_working_dir = working_dir

    tags_path = os.path.join(working_dir, "tags")
    if not os.path.isfile(tags_path):
        return

    tokens = {}
    with open(tags_path) as fh:
        for line in fh.readlines():
            if line.startswith("!"):
                continue

            token = line[:line.find("\t")]
            for subtoken in split_token(token):
                tokens[subtoken] = subtoken

    ctx.lists["user.code_mode_project_token"] = tokens


ui.register("win_focus", update_list)
