title: /Evolution/
-
folder select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("35 108 73 -164", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)

item select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("343 138 378 450", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)

message create:
    key(ctrl-shift-m)

message reply:
    key(ctrl-r)

message reply all:
    key(ctrl-shift-r)

main up:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative(".", "-200")
    mouse_scroll(-5)
    user.mouse_helper_position_restore()

main down:
    user.mouse_helper_position_save()
    user.mouse_helper_move_active_window_relative(".", "-200")
    mouse_scroll(5)
    user.mouse_helper_position_restore()
