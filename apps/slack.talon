title: /^Slack/
-
main down:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative(".", "-328")
    mouse_scroll(5)
    user.mouse_pos_restore()

main up:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative(".", "-328")
    mouse_scroll(-5)
    user.mouse_pos_restore()

folder select:
    user.telector_show("active_window:2 201 54 -2", "explicit_colors:#4d394b", "lines")

folder down:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative("64", ".")
    mouse_scroll(5)
    user.mouse_pos_restore()

folder up:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative("64", ".")
    mouse_scroll(-5)
    user.mouse_pos_restore()

main focus:
    user.mouse_pos_save()
    user.mouse_move_image_relative("slack/message-corner.png", 55, 10, 0)
    mouse_click(0)
    user.mouse_pos_restore()

side focus:
    user.mouse_pos_save()
    user.mouse_move_image_relative("slack/message-corner.png", 30, 10, 1)
    mouse_click(0)
    user.mouse_pos_restore()

side close:
    user.mouse_pos_save()
    user.mouse_move_image_relative("slack/close-icon.png", 0, 0)
    mouse_click(0)
    sleep(0.1)
    user.mouse_pos_restore()

side down:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative("-36", "622")
    mouse_scroll(5)
    user.mouse_pos_restore()

side up:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative("-36", "622")
    mouse_scroll(-5)
    user.mouse_pos_restore()
