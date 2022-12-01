app.exe: kitty
-
tag(): terminal
tag(): user.generic_unix_shell
clear word left:
    key(ctrl-w)
clear word right:
    edit.word_right()
    key(ctrl-w)
matcha hash:
    key(ctrl-shift-p h)
matcha web:
    key(ctrl-shift-p y)
matcha path:
    key(ctrl-shift-p f)
buffer paginate:
    key(ctrl-shift-h)
buffer vim:
    key(ctrl-shift-i)
settings():
    user.mouse_wheel_down_amount = 20
