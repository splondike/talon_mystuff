title: /Evolution/
-
# settings():
#     user.telector_debug_mode = 1
#     user.telector_bounding_box = "active_window:310 70 370 400"
#     user.telector_background_detector = "explicit_colors:#ffffff #eeeeee"
#     user.telector_target_mode = "lines"

folder select:
    user.telector_show("active_window:0 110 216 -174", "explicit_colors:#ffffff", "lines")

item select:
    user.telector_show("active_window:310 70 370 400", "explicit_colors:#ffffff #eeeeee", "lines")

message create:
    key(ctrl-shift-m)

message reply:
    key(ctrl-r)

message reply all:
    key(ctrl-shift-r)

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
