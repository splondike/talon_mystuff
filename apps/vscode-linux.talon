os: linux
and title: /Visual Studio Code$/
-
swap: key(ctrl-tab)

swap files: key(ctrl-p)

swap recent: user.vscode_and_wait("workbench.action.showAllEditorsByMostRecentlyUsed")

search grep: key(ctrl-shift-f)

search symbol: key(ctrl-t)

go row <digit_string>:
    key(ctrl-g)
    insert(digit_string)
    key(enter)
    key(home)

move row up: key(alt-up)

move row down: key(alt-down)

outline show:
    user.vscode_and_wait("outline.focus")
    # This is to give keyboard focus so we can search
    repeat(1)

project show:
    user.vscode_and_wait("workbench.view.explorer")
    user.vscode_and_wait("outline.removeView")

mark <number_small>: key("ctrl-shift-{number_small}")
jump <number_small>: key("ctrl-{number_small}")

folder hide: user.vscode_and_wait("workbench.action.closeSidebar")

file save: key(ctrl-s)

folder select:
    bounding_rectangle = user.mouse_helper_calculate_relative_rect("-319 78 -270 -1", "active_window")
    user.mouse_helper_blob_picker(bounding_rectangle)

tags expand: user.vscode_and_wait("editor.emmet.action.expandAbbreviation")

execute that:
    key(ctrl-s)
    user.system_command("i3-msg focus left")
    key(up enter)
    user.system_command("i3-msg focus right")

chip:
    edit.undo()