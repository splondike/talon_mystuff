-
copy mouse info: user.copy_mouse_info()

mouse left:
    user.mouse_move_relative(-20, 0)
    user.grid_close()
mouse right:
    user.mouse_move_relative(20, 0)
    user.grid_close()
mouse down:
    user.mouse_move_relative(0, 20)
    user.grid_close()
mouse up:
    user.mouse_move_relative(0, -20)
    user.grid_close()
