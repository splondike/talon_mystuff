title: /Squareweave Mail/
-
item select:
    user.telector_show("active_window:357 234 531 -4", "explicit_colors:#ffffff #c2dbff #f4f7f7 #e2e8ea", "lines")

item mark unread:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative("484", "161")
    mouse_click(0)
    user.mouse_pos_restore()

navigate inbox:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative("115", "225")
    sleep(0.1)
    mouse_click(0)
    sleep(0.1)
    user.mouse_pos_restore()

navigate next:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative("-81", "157")
    mouse_click(0)
    user.mouse_pos_restore()

navigate previous:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative("-43", "157")
    mouse_click(0)
    user.mouse_pos_restore()

main down:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative(".", "-10")
    mouse_scroll(5)
    user.mouse_pos_restore()

main up:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative(".", "-10")
    mouse_scroll(-5)
    user.mouse_pos_restore()
