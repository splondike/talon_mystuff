title: /The Battle for Wesnoth/
-
game grid show: user.wesnoth_grid_show()
game grid hide: user.wesnoth_grid_hide()

recruit unit: key(ctrl-r)
recall unit: key(alt-r)
next unit: key(n)
end turn: key(ctrl-space)
unselect unit:
    # Not 0, 0 because that scrolls
    mouse_move(1, 1)
    key(f11)

move <user.letter> <number_small>:
    user.wesnoth_grid_mouse_move("{letter}{number_small}")

click <user.letter> <number_small>:
    user.wesnoth_grid_mouse_move("{letter}{number_small}")
    mouse_click(0)

scroll left: mouse_scroll(0, -1, 1)
scroll right: mouse_scroll(0, 1, 1)
scroll up: mouse_scroll(-1, 0, 1)
scroll down: mouse_scroll(1, 0, 1)

action(user.pop): mouse_click(0)
