app: disciples2
user.disciples2_screen: world
-
map <user.disciples2_map_move>:
    xcoord = user.ts_array_get(disciples2_map_move, 0)
    ycoord = user.ts_array_get(disciples2_map_move, 1)
    user.mouse_helper_move_active_window_relative(xcoord, ycoord)
    sleep(32ms)
    mouse_click()
    sleep(32ms)
    user.mouse_helper_move_active_window_relative("-5", "-5")

parse screen:
    user.disciples2_parse_screen()
