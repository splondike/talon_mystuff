title: /Gmail/
-
item select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("541 271 587 -1", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)

item mark unread:
    user.mouse_helper_position_save()
    user.mouse_helper_position_active_window_relative("484", "161")
    mouse_click(0)
    user.mouse_helper_position_restore()

navigate inbox:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative("63", "266")
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()

navigate next:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative("-143", "191")
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()

navigate last:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative("-102", "191")
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()

main down:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative(".", "-10")
    mouse_scroll(5)
    user.mouse_helper_position_restore()

main up:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative(".", "-10")
    mouse_scroll(-5)
    user.mouse_helper_position_restore()
