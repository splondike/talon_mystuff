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

main up:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative(".", ".")
    mouse_scroll(-5, 0)
    user.mouse_helper_position_restore()

main down:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative(".", ".")
    mouse_scroll(5, 0)
    user.mouse_helper_position_restore()
