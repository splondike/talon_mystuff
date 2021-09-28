title: /QuiteRSS/
-
folder select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("25 56 49 -27", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)

folder refresh:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2021-09-25_17.18.31.599112.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()

item select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("233 54 258 327", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)

main up:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative(".", "-50")
    mouse_scroll(-5, 0)
    user.mouse_helper_position_restore()

main down:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative(".", "-50")
    mouse_scroll(5, 0)
    user.mouse_helper_position_restore()

page visit:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative("197", "265")
    mouse_click(0)
    use.mouse_helper_position_restore()

page copy:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative("197", "265")
    mouse_click(1)
    key(down)
    key(down)
    key(down)
    key(down)
    key(enter)
    user.mouse_helper_position_restore()
