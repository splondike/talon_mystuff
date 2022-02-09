action(user.pop): core.repeat_command(1)
sleep: sleep(1s)

# Use micro prefix since knausj uses macro prefix
micro file view: user.macro_show_macro_file("view")
micro file edit: user.macro_show_macro_file("edit")
micro file reset: user.macro_reset()

micro append click: user.macro_append("mouse click relative")
micro append sleep: user.macro_append("sleep")
micro append screen change: user.macro_append("screen change")
^micro append port <number_small>$: user.macro_append("port", "{number_small}")
^micro append key <user.modifiers> <user.unmodified_key>$: user.macro_append("key", "{modifiers}-{unmodified_key}")
^micro append key <user.unmodified_key>$: user.macro_append("key", "{unmodified_key}")
