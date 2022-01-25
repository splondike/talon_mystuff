action(user.pop): core.repeat_command(1)
sleep: sleep(1s)

# Use micro prefix since knausj uses macro prefix
micro file view: user.macro_show_macro_file("view")
micro file edit: user.macro_show_macro_file("edit")
micro file reset: user.macro_reset()

micro append click: user.macro_append("mouse click relative")
micro append sleep: user.macro_append("sleep")
micro append screen change: user.macro_append("screen change")
