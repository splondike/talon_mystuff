app.exe: urxvt
-
git rebase main:
    insert("git rebase origin/main")
    key("enter")

git add:
    insert("git add ")

git commit inline:
    insert("git commit -m \"\"")
    key("left")

git status:
    insert("git status")
    key("enter")

vim:
    insert("vim")
    key("enter")

list files:
    insert("ls")
    key("enter")

list all files:
    insert("ls -al")
    key("enter")

source environment:
    insert("source venv/bin/activate")
    key("alt-b")
    key("alt-b")
    key("alt-b")

ship insert:
    key('shift-insert')
