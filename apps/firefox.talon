title: /Mozilla Firefox/
-
wheel down:
    user.mouse_scroll_down()
    user.mouse_scroll_down()

wheel up:
    user.mouse_scroll_up()
    user.mouse_scroll_up()

google <phrase>:
    key(ctrl-t g space)
    insert(phrase)
    key(enter)

item select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("112 235 161 -3", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)

develop toggle: key(ctrl-shift-i)

develop inspector: key(ctrl-shift-c)

develop console: key(ctrl-shift-k)

develop console clear:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2022-01-26_19.37.26.424968.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()
