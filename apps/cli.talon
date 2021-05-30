app.exe: urxvt
-
git fetch:
    insert("git fetch")
    key("enter")

git rebase main:
    insert("git rebase origin/main")

git add:
    insert("git add ")

git commit:
    insert("git commit")
    key("enter")

git commit inline:
    insert("git commit -m \"\"")
    key("left")

git status:
    insert("git status")
    key("enter")

git checkout:
    insert("git checkout feature/")

git push origin:
    insert("git push origin ")

git diff:
    insert("git diff HEAD^..HEAD")

git log:
    insert("git log")
    key("enter")

docker compose exec backend:
    insert("docker-compose exec backend bash")
    key("enter")

docker compose exec frontend:
    insert("docker-compose exec backend bash")
    key("enter")

docker compose exec database:
    insert("docker-compose exec database bash")
    key("enter")

docker compose run backend:
    insert("docker-compose run --rm backend bash")
    key("enter")

docker compose up:
    insert("docker-compose up")
    key("enter")

run vim:
    insert("vim")
    key("enter")

run my sequel:
    insert("mysql")
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

source machine learning:
    insert("source ~/Desktop/machine-learning-venv/bin/activate")
    key(enter)

change directory talon:
    insert("cd ~/.talon/user/mystuff")
    key(enter)

ship insert:
    key('shift-insert')
