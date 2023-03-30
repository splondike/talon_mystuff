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
matcha path:
    key(ctrl-alt-p f)
matcha kebab:
    key(ctrl-alt-p s)

buffer paginate:
    key(ctrl-alt-h)
buffer vim:
    key(ctrl-alt-i)
buffer duplicate:
    key(ctrl-alt-f)
