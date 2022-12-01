title: /^VIM i/
-
spammer: ", "

pour this:
    key(end)
    key(enter)

complete [next]: key(ctrl-n)
complete : key(ctrl-p)

jump back:
    key(escape)
    "?"

jump back <user.word>:
    key(escape)
    insert("?" + word)
    key(enter)

jump forward <user.word>:
    key(escape)
    insert("/" + word)
    key(enter)
