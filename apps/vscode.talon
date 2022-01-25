title: /Visual Studio Code$/
-
swap: key(ctrl-tab)

swap files: key(ctrl-p)

swap recent: user.vscode_and_wait("workbench.action.quickOpenPreviousRecentlyUsedEditorInGroup")

search grep: key(ctrl-t)

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

terminal show:
    key(ctrl-`)

mark <number_small>: key("ctrl-shift-{number_small}")
jump <number_small>: key("ctrl-{number_small}")

sidebar hide: user.vscode_and_wait("workbench.action.closeSidebar")

file save: key(ctrl-s)
