os: mac
-
port <number_small>: key("alt-{number_small}")
port ten: key(alt-0)
move win port <number_small>: user.system_command("/opt/homebrew/bin/yabai -m window --space {number_small}")

win right: user.system_command("/Users/stefansk/osx-scripts/scripts/yabai-stack-aware.py focus east")
win left: user.system_command("/Users/stefansk/osx-scripts/scripts/yabai-stack-aware.py focus west")
win up: user.system_command("/Users/stefansk/osx-scripts/scripts/yabai-stack-aware.py focus north")
win down: user.system_command("/Users/stefansk/osx-scripts/scripts/yabai-stack-aware.py focus south")

move win right: user.system_command("/opt/homebrew/bin/yabai -m window --warp east")
move win left: user.system_command("/opt/homebrew/bin/yabai -m window --warp west")
move win up: user.system_command("/opt/homebrew/bin/yabai -m window --warp north")
move win down: user.system_command("/opt/homebrew/bin/yabai -m window --warp south")

launch: key(alt-p)
launch term: key(alt-enter)
win kill: user.system_command("/opt/homebrew/bin/yabai -m window --close")
