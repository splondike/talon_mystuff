os: mac
and app.bundle: com.microsoft.VSCode
-
swap: key(ctrl-tab)

swap files: key(super-p)

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

mark <number_small>: key("super-shift-{number_small}")
jump <number_small>: key("super-{number_small}")

folder hide: user.vscode_and_wait("workbench.action.closeSidebar")

file save: key(super-s)

tags expand: user.vscode_and_wait("editor.emmet.action.expandAbbreviation")

chip:
    edit.undo()
