user.window_role: GtkFileChooserDialog
user.file_chooser_dialog_type: open
-
seedy up: key(alt-up)

seedy down: key(alt-down)

folder select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("5 2 43 -84", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)

item select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("191 28 217 -82", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)
