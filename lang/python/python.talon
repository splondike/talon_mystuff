mode: user.python
mode: command
and code.language: python
-
dock block:
    insert('"""')
    key(enter)
    insert('"""')
    key(up end enter)

row push:
    key(end)
    insert(":")
    key(enter)

state lambda: "lambda"
op in: " in "
