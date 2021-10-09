title: /^VIM/
-
settings():
    # Allow you to tweak the detected bounding box, default is just the window
    user.telector_bounding_box = "active_window:30 0 -10 -0"
    # Would be mouse_fill, background, pixel_fill
    user.telector_background_detector = "explicit_colors:#252525"
    # user.telector_debug_mode = 1
    user.telector_word_spacing = 10

# Floodfill from mouse cursor, relative to window, relative to image, floodfill from text cursor
# Selection colours (find text within these)
# Background colours (drop these right at start)

save that:
    key(escape)
    insert(":w")
    key(enter)

edit file:
    key(escape)
    insert(":e ")

ddent:
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

jump back:
    "?"

jump back <user.word>:
    insert("?" + word)
    key(enter)

jump forward <user.word>:
    insert("/" + word)
    key(enter)
