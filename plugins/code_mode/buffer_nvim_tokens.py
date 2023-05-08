"""
Populates the code mode project tokens from the currently focussed buffer.
"""

import os
import re

from talon import actions, ui, cron, Context

ctx = Context()
ctx.matches = r"""
title: /^VIM/i
"""


last_working_dir = None
cron_handle = None
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


def calculate_tokens(contents):
    rtn = set()
    letter_segments = re.sub("[^a-zA-Z]", " ", contents).split(" ")
    for letter_segment in letter_segments:
        for word in split_token(letter_segment):
            rtn.add(word)

    return rtn


def _populate_list():
    # Just do the first 1000 lines to avoid stalling on long files
    buffer_contents = actions.user.vim_call_rpc_function(
        "join(getline(0, 1000))"
    )

    ctx.lists["user.code_mode_project_token"] = calculate_tokens(
        buffer_contents
    )


def toggle_timer(window):
    global cron_handle

    if window.title.startswith("VIM"):
        cron_handle = cron.interval("10s", _populate_list)
        _populate_list()
    else:
        cron.cancel(cron_handle)


ui.register("win_focus", toggle_timer)
