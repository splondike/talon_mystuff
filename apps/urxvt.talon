app: URxvt
-
clear word left:
    key(ctrl-w)
clear word right:
    edit.word_right()
    key(ctrl-w)
action(edit.line_start): key(ctrl-a)
action(edit.line_end): key(ctrl-e)
action(edit.word_left): key(alt-b)
action(edit.word_right): key(alt-f)
action(edit.delete_line):
    edit.line_start()
    key(ctrl-k)
