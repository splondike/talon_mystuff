title: Disciples II
-
game save:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2022-01-02_14.17.37.835439.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(1)

    user.mouse_helper_move_image_relative("2022-01-02_14.18.34.427288.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(1)

    # This is the Game1 game
    user.mouse_helper_move_image_relative("2022-01-02_14.19.23.579012.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)

    key(enter)
    sleep(0.1)
    key(enter)
    sleep(2)
    key(enter)
    sleep(0.1)
    key(escape)

    user.mouse_helper_position_restore()

game load:
    user.mouse_helper_position_save()
    user.mouse_helper_move_image_relative("2022-01-02_14.17.37.835439.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(1)

    user.mouse_helper_move_image_relative("2022-01-02_14.22.24.618163.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(1)

    # This is the Game1 game
    user.mouse_helper_move_image_relative("2022-01-02_14.19.23.579012.png", 0)
    sleep(0.05)
    mouse_click(0)
    sleep(0.05)

    key(enter)
    sleep(0.1)
    key(enter)
    sleep(3)
    key(escape)
    sleep(1)
    key(escape)

    user.mouse_helper_position_restore()

unit <number_small>:
    user.disciples_unit_select(number_small)

unit sleep round:
    key(d)
    sleep(2)
    key(d)
    sleep(2)
    key(d)
    sleep(2)
    key(d)
    sleep(2)
    key(d)

structures show:
    key(a)
    sleep(1)
    user.mouse_helper_move_active_window_relative("200", "200")
    mouse_click(0)

