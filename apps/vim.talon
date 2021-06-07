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
    key('d')
    key('d')

spammer: ", "

complete [next]: key(ctrl-n)
complete previous: key(ctrl-p)

swap: ",s"

swap recent: ",t"

swap files: ",f"

action(edit.indent_less): "<<"
action(edit.indent_more): ">>"

search grep:
    key(escape)
    insert(":Rg ")

search grep <user.text>:
    key(escape)
    insert(":Rg {text}")

action(edit.redo):
    key(escape)
    key(shift-z)

action(edit.undo):
    key(escape)
    key(z)

move row up: key(ctrl-f)
move row down: key(ctrl-s)

slapper:
    key(end)
    key(enter)

go row <digit_string>:
    key(escape)
    insert(":" + digit_string)
    key(enter)
