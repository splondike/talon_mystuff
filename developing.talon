title: /^VIM/
-
rerun:
    user.vim_normal_mode()
    insert(":w")
    key(enter)
    sleep(0.1)

    user.system_command("i3-msg focus left")
    key(up enter)
    user.system_command("i3-msg focus right")
