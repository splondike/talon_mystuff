title: Signal
-
folder select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("10 73 57 -3", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)

main up:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative("371", "78")
    mouse_scroll(-5, 0)
    user.mouse_helper_position_restore()

main down:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative("371", "78")
    mouse_scroll(5, 0)
    user.mouse_helper_position_restore()
