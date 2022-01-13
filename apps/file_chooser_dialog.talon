user.window_role: GtkFileChooserDialog
-
seedy up: key(alt-up)

seedy down: key(alt-down)

folder select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("6 2 31 -3", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)

file select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("187 127 214 -92", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)

name select:
    key(tab:4)