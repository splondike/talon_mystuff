# I don't use most of the commands defined in the knausj repository

port <number_small>: user.system_command("i3-msg workspace {number_small}")
port ten: user.system_command("i3-msg workspace 10")
port swap: user.system_command("i3-msg workspace back_and_forth")

win left: user.system_command("i3-msg focus left")
win right: user.system_command("i3-msg focus right")
win up: user.system_command("i3-msg focus up")
win down: user.system_command("i3-msg focus down")
win kill: user.system_command("i3-msg kill")

move win port <number_small>:  user.system_command("i3-msg move container to workspace {number_small}")
move win port ten: user.system_command("i3-msg move container to workspace 10")
move win left: user.system_command("i3-msg move left")
move win right: user.system_command("i3-msg move right")
move win up: user.system_command("i3-msg move up")
move win down: user.system_command"i3-msg move down")

launch: key(alt-p)