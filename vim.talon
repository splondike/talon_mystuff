title: /- G?VIM/
-
settings():
    # Allow you to tweak the detected bounding box, default is just the window
    user.telector_bounding_box = "active_window:30 0 -10 -0"
    # Would be mouse_fill, background, pixel_fill
    user.telector_background_detector = "explicit_colors:#252525"
    # user.telector_debug_mode = 1
    user.telector_word_spacing = 10

# Floodfill from mouse cursor, relative to window, relative to image, floodfill from text cursor
# Selection colours (find text within these)
# Background colours (drop these right at start)

save that:
    key(escape)
    insert(":w")
    key(enter)

ddent:
    key('d')
    key('d')
