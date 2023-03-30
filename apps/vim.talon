title: /^VIM/
-
file save:
    key(escape)
    insert(":w")
    key(enter)

file edit:
    user.vim_normal_mode()
    insert(":e ")

file edit relative:
    user.vim_normal_mode()
    insert(":e;")

swap:
    key(escape)
    key("ctrl-6")

swap recent:
    key(escape)
    insert(":Buffers")
    key(return)

swap files:
    key(escape)
    insert(":Files")
    key(return)

search grep:
    key(escape)
    insert(":Rg ")

search grep <user.text>:
    key(escape)
    insert(":Rg {text}")

move row up: key(ctrl-f)
move row down: key(ctrl-s)

# Movement and editing, primarily anchored to line numbers.
# jump take chuck change comment ?bring?. Probably want to abstract all the non-jump ones to avoid repetition.

centre that:
    user.vim_normal_mode()
    key("h z")

jump <user.vim_jump_symbol>:
    user.vim_normal_mode()
    key("f {vim_jump_symbol}")
    sleep(0.1)

jump <digit_string> [<user.vim_jump_symbol>]:
    user.vim_normal_mode()
    insert(":" + digit_string)
    key(enter)
    sleep(0.1)
    next = vim_jump_symbol or "escape"
    key("f {next}")
    sleep(0.1)

take <digits>:
    user.vim_normal_mode()
    user.vim_select_rows(digits)

take <digits> through <digits>:
    user.vim_normal_mode()
    user.vim_select_rows(digits_1, digits_2)
