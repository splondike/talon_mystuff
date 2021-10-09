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

search focus:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2021-09-28_16.54.43.883337.png", 0, 97, 2)
    mouse_click(0)
    key(end)
    user.mouse_helper_position_restore()

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
