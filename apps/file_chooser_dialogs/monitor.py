from talon import actions, settings, Module

mod = Module()

FILE_SAVE_HASH = "9b1e4170a4bb3e8b8571"

setting_scrape_screen = mod.setting(
    "file_chooser_dialogs_active",
    type=int,
    desc="Used to trigger a run of file_chooser_dialog_scope",
    default=0
)

@mod.scope
def file_chooser_dialog_scope():
    if setting_scrape_screen.get() == 0:
        return {
            "file_chooser_dialog_type": "hidden"
        }

    bounding_rectangle = actions.user.mouse_helper_calculate_relative_rect(
        "2 2 59 42",
        "active_window"
    )
    curr_hash = actions.user.mouse_helper_calculate_rectangle_hash(
        bounding_rectangle
    )
    print("HOwdy", curr_hash)
    return {
        "file_chooser_dialog_type":
            "save" if curr_hash == FILE_SAVE_HASH else "open"
    }


settings.register("user.file_chooser_dialogs_active", file_chooser_dialog_scope.update)
