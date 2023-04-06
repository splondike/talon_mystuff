title: /^VIM/
-
settings():
    # Vim seems to get its keys jumbled above this speed
    key_wait = 2

file save:
    user.vim_normal_mode()
    insert(":w")
    key(enter)

file edit:
    user.vim_normal_mode()
    insert(":e ")

file edit relative:
    user.vim_normal_mode()
    insert(":e;")

swap:
    user.vim_normal_mode()
    key("ctrl-6")

swap recent:
    user.vim_normal_mode()
    insert(":Buffers")
    key(return)

swap files:
    user.vim_normal_mode()
    insert(":Files")
    key(return)

search grep:
    user.vim_normal_mode()
    insert(":Rg ")

search grep <user.text>:
    user.vim_normal_mode()
    insert(":Rg {text}")

centre that:
    user.vim_normal_mode()
    key("h z")

chip:
    edit.undo()

pour this:
    user.vim_normal_mode()
    key("o")

mark:
    user.vim_normal_mode()
    key("m a")

mark bat:
    user.vim_normal_mode()
    key("m b")

# Movement and editing, primarily anchored to line numbers.
# jump take chuck change comment ?bring?. Probably want to abstract all the non-jump ones to avoid repetition.

jump mark:
    user.vim_normal_mode()
    key("` a")

jump mark bat:
    user.vim_normal_mode()
    key("` b")

jump <user.vim_jump_position>:
    user.vim_jump(vim_jump_position)

change row:
    user.vim_normal_mode()
    key("r r")

change {user.vim_text_object}:
    user.vim_normal_mode()
    key("r {vim_text_object}")

chuck row:
    user.vim_normal_mode()
    key("d d")

take row:
    user.vim_normal_mode()
    key("A")

take {user.vim_text_object}:
    user.vim_normal_mode()
    key("a {vim_text_object}")

# TODO: take mark pair to select between two marks. Good for folds

bring <user.vim_bring_range>:
    user.vim_bring(vim_bring_range)

# TODO: Finish folds
fold that:
    user.vim_normal_mode()
    key("h f")

fold open:
    user.vim_normal_mode()
    key("h o")

# TODO:
# * Got to have a way to pick a line in fzf. No option built in. Approaches are to add the feature, add in line num to the fzf input, exploit geom of terminal and draw with Talon. Probably the first is easiest.

# bring 15 - Bring line 15
# bring 15 through 20 - Bring lines 15 through 20
# bring 15 red through right paren - Bring the token starting with 'r' through to the next right parenthesis
# bring 15 red through gust each - Bring the token starting with 'r' through to the end of the next token staring with 'ge'
# bring 15 dubquote - Bring the whole first double quoted string on the line
# bring 15 args - Bring the whole first paren wrapped arguments (maybe multiline)
# bring 15 block - Bring the whole block around line 15
# take and change would be very similar to this I think

# comment 15
# comment 15 through 20
# comment 15 block

# Could use easymotion to select a word or a phrase to bring
# Take, chuck, change would be the same as bring. comment would just have the 
# lines stuff (and maybe block or function if somebody's made a good text object)
# Can call the easymotion picker using (see autoload/EasyMotion.vim):
# * call EasyMotion#S(1, 0, 2)
# * call EasyMotion#User('myregex...', 0, 2, 0)
# /\W\zssh.\{-}\Wr.\{-}\ze\W - match a token starting with sh up to the end of one starting with r
# Can probably quite often just bring a given line to the clipboard to work out
# what to bring or select etc.

move row up: key(ctrl-f)
move row down: key(ctrl-s)
