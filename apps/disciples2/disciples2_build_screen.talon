app: disciples2
user.disciples2_screen: build
-
struct pick:
    matches = user.mouse_helper_find_template_relative("2022-02-12_00.32.21.728029.png", -41, -28)
    user.marker_ui_show(matches)

struct castle:
    user.mouse_helper_move_active_window_relative("581", "552")
    sleep(16ms)
    mouse_click()
    user.mouse_helper_move_active_window_relative("-1", "-1")

struct sword:
    user.mouse_helper_move_active_window_relative("585", "502")
    sleep(16ms)
    mouse_click()
    user.mouse_helper_move_active_window_relative("-1", "-1")

struct magic:
    user.mouse_helper_move_active_window_relative("627", "475")
    sleep(16ms)
    mouse_click()
    user.mouse_helper_move_active_window_relative("-1", "-1")

struct arrow:
    user.mouse_helper_move_active_window_relative("659", "500")
    sleep(16ms)
    mouse_click()
    user.mouse_helper_move_active_window_relative("-1", "-1")

struct swirl:
    user.mouse_helper_move_active_window_relative("659", "542")
    sleep(16ms)
    mouse_click()
    user.mouse_helper_move_active_window_relative("-1", "-1")
