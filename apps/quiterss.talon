title: /QuiteRSS/
-
folder select:
    user.telector_show("active_window:6 58 46 -51", "explicit_colors:#ffffff #0000ff #308cc6", "lines")

item select:
    user.telector_show("active_window:229 55 248 235", "explicit_colors:#ffffff #0000ff #308cc6", "lines")

main up:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative(".", "-50")
    mouse_scroll(-5)
    user.mouse_pos_restore()

main down:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative(".", "-50")
    mouse_scroll(5)
    user.mouse_pos_restore()

page visit:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative("197", "265")
    mouse_click(0)
    use.mouse_pos_restore()

page copy:
    user.mouse_pos_save()
    user.mouse_pos_active_window_relative("197", "265")
    mouse_click(1)
    user.mouse_pos_restore()
    key(down)
    key(down)
    key(down)
    key(down)
    key(enter)
