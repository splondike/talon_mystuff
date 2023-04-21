app.exe: kitty
-
git clone:
    insert("git clone ")

git fetch:
    insert("git fetch")
    key("enter")

git rebase master:
    insert("git rebase origin/master")

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

git push:
    insert("git push origin ")

get pull:
    insert("git pull ")
    key("enter")

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
    insert("nvim")
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

change directory knaus:
    insert("cd ~/.talon/user/knausj_talon")
    key(enter)

change directory talon:
    insert("cd ~/.talon/user/talon_mystuff")
    key(enter)

cd up: "cd ../"

cd up <number_small>$:
    dots = user.repeat_text("../", number_small)
    insert("cd " + dots)

cd search$:
    # Uses fzf's bash completion with `fd` to change directory
    key(alt-c)

cd search <phrase>$:
    # Uses fzf's bash completion with `fd` to change directory
    key(alt-c)
    insert(phrase)

cd change:
    insert("cd ")
    key(tab tab)
    sleep(0.1)
    key(ctrl-alt-p w)

file path insert:
    # Uses fzf's bash completion with `fd` to insert a file path
    key(ctrl-t)

ship insert:
    key('shift-insert')

cube context:
    insert("kubectx")
    key("enter")

cube namespaces:
    insert("kubectl get ns")
    key("enter")

cube pods:
    insert("kubectl get pods --namespace=")
