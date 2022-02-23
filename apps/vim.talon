title: /^VIM/
-
# Floodfill from mouse cursor, relative to window, relative to image, floodfill from text cursor
# Selection colours (find text within these)
# Background colours (drop these right at start)

file save:
    key(escape)
    insert(":w")
    key(enter)

file edit:
    key(escape)
    insert(":e ")

chuck line:
    key(escape)
    key('d')
    key('d')

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

action(edit.indent_less): "<<"
action(edit.indent_more): ">>"

search grep:
    key(escape)
    insert(":Rg ")

search grep <user.text>:
    key(escape)
    insert(":Rg {text}")

action(edit.redo):
    key(shift-z)

action(edit.undo):
    key(z)

move row up: key(ctrl-f)
move row down: key(ctrl-s)

go row <digit_string>:
    key(escape)
    insert(":" + digit_string)
    key(enter)
    key(^)

go symbol <user.any_alphanumeric_key>:
    key(escape)
    insert("f")
    insert(any_alphanumeric_key)

select row <digits>:
    user.vim_select_rows(digits)

select row <digits> through <digits>:
    user.vim_select_rows(digits_1, digits_2)

replace between dubquote:
    insert('rs"')

replace between quote:
    insert("rs'")

replace between paren:
    insert("rs(")

back word:
    user.vim_normal_mode()
    key(l)

jump back:
    "?"

jump back <user.word>:
    insert("?" + word)
    key(enter)

jump forward <user.word>:
    insert("/" + word)
    key(enter)
