title: /Slack$/
title: /- Slack -/
-
main down:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative(".", "-328")
    mouse_scroll(5)
    user.mouse_helper_position_restore()

main up:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative(".", "-328")
    mouse_scroll(-5)
    user.mouse_helper_position_restore()

folder select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("18 195 47 -49", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)

folder down:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative("64", ".")
    mouse_scroll(5)
    user.mouse_helper_position_restore()

folder up:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative("64", ".")
    mouse_scroll(-5)
    user.mouse_helper_position_restore()

main focus:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2021-09-28_11.58.50.914640.png", 0, 0, -35)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()

side focus:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2021-09-28_11.58.50.914640.png", 1, 0, -35)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)
    user.mouse_helper_position_restore()

side close:
    key(ctrl-.)

side down:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative("-36", "622")
    mouse_scroll(5)
    user.mouse_helper_position_restore()

side up:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative("-36", "622")
    mouse_scroll(-5)
    user.mouse_helper_position_restore()
