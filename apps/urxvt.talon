app: URxvt
-
clear word left:
    key(ctrl-w)
clear word right:
    edit.word_right()
    key(ctrl-w)
action(edit.line_start): key(ctrl-a)
action(edit.line_end): key(ctrl-e)
action(edit.word_left): key(alt-b)
action(edit.word_right): key(alt-f)
action(edit.delete_line):
    edit.line_start()
    key(ctrl-k)

settings():
    # Allow you to tweak the detected bounding box, default is just the window
    user.telector_bounding_box = "active_window:0 0 -10 -0"
    # Would be mouse_fill, background, pixel_fill
    user.telector_background_detector = "explicit_colors:#252525"
    user.telector_selection_background = "#ffffff"
    # user.telector_debug_mode = 1

