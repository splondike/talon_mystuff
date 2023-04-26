title: /^VIM/
-
tag(): user.code_mode_active
settings():
    # Vim seems to get its keys jumbled above this speed
    key_wait = 2

file save:
    user.vim_normal_mode()
    insert(":w")
    key(enter)

file editor exit:
    user.vim_normal_mode()
    insert(":q")
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

swap recent [<user.word>]:
    user.vim_escape_insert_keys(", t")
    insert(word or "")

swap files [<user.word>]:
    user.vim_escape_insert_keys(", f")
    insert(word or "")

search grep [<user.word>]:
    user.vim_escape_insert_keys(", g")
    insert(word or "")

search functions [<user.word>]:
    user.vim_escape_insert_keys(", d")
    insert(word or "")

centre that:
    user.vim_escape_insert_keys("h z")

chip:
    edit.undo()

pour that:
    user.vim_escape_insert_keys("o")

mark [<user.letter>]:
    mark_name = letter or "a"
    user.vim_escape_insert_keys("m {mark_name}")

insert:
    user.vim_insert_mode()

move row up: user.vim_escape_insert_keys("ctrl-f")
move row down: user.vim_escape_insert_keys("ctrl-s")

# Movement and editing, primarily anchored to line numbers.

jump mark [<user.letter>]:
    mark_name = letter or "a"
    user.vim_escape_insert_keys("` {mark_name}")

jump <user.vim_jump_position>:
    user.vim_jump(vim_jump_position)

jump <user.vim_jump_position> insert:
    is_start_of_word = user.vim_jump(vim_jump_position)
    user.vim_insert_mode(is_start_of_word)

back <user.vim_jump_position>:
    user.vim_jump(vim_jump_position, 0)

follow (<user.letter> | <user.symbol_key>):
    key1 = letter or ""
    key2 = symbol_key or ""
    user.vim_escape_insert_keys("f {key1}{key2}")

change row:
    user.vim_normal_mode()
    key("r r")

change {user.vim_text_object}:
    user.vim_escape_insert_keys("r {vim_text_object}")

chuck row:
    user.vim_normal_mode()
    key("d d")

chuck that:
    user.vim_escape_insert_keys("d")

chuck {user.vim_text_object}:
    user.vim_normal_mode()
    key("d {vim_text_object}")

take row:
    user.vim_visual_line_mode()

take {user.vim_text_object}:
    user.vim_normal_mode()
    key("a {vim_text_object}")

take <user.vim_line_range>:
    user.vim_take_line_range(vim_line_range)

bring <user.vim_bring_range>:
    user.vim_bring(vim_bring_range)

pull:
    edit.copy()
    user.vim_go_mark("z")
    edit.paste()

comment that:
    user.vim_normal_mode()
    key(, c c escape)

comment <user.vim_line_range>:
    user.vim_take_line_range(vim_line_range)
    key(, c c escape)

fold that:
    user.vim_escape_insert_keys("h f")

fold open:
    user.vim_escape_insert_keys("h O")

fold close:
    user.vim_escape_insert_keys("h C")

fold max:
    user.vim_escape_insert_keys("h M")

fold min:
    user.vim_escape_insert_keys("h R")

fold chuck:
    user.vim_escape_insert_keys("h d")

chuck left:
    user.vim_escape_insert_keys("r b")

chuck right:
    user.vim_escape_insert_keys("r w")

# TODO:
# * Got to have a way to pick a line in fzf. No option built in. Approaches are to add the feature, add in line num to the fzf input, exploit geom of terminal and draw with Talon. Probably the first is easiest.
# * Might be able to use two different words for jumping up and down and thereby cover a range of twenty lines with a single number
# * Temporary rewrite rule. If I'm using a particular phrase or homophone all the time in a particular document it would be nice to temporarily add it to 'words to replace' or 'additional words'.
# * Periodically grab buffer and run it through a word splitter to get tokens for stack.
# * Vim helper that show tokens nearby to the current cursor position so you don't have to say them. Though maybe this is a crutch for stack not working as well as hoped.
