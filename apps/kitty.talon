app.exe: kitty
-
tag(): terminal
tag(): user.generic_unix_shell

settings():
    user.mouse_wheel_down_amount = 20

clear word left:
    key(ctrl-w)
clear word right:
    edit.word_right()
    key(ctrl-w)

matcha hash:
    key(ctrl-alt-p h)
matcha web:
    key(ctrl-alt-p y)
matcha file:
    key(ctrl-alt-p f)
matcha kebab:
    key(ctrl-alt-p s)
matcha copy hash:
    key(ctrl-alt-c h)
matcha copy web:
    key(ctrl-alt-c y)
matcha copy file:
    key(ctrl-alt-c f)
matcha copy kebab:
    key(ctrl-alt-c s)

buffer paginate:
    key(ctrl-alt-h)
buffer vim:
    key(ctrl-alt-i)
buffer duplicate:
    key(ctrl-alt-f)
