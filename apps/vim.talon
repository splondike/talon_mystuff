title: /^VIM/
-
tag(): user.code_mode_active
settings():
    # Vim seems to get its keys jumbled above this speed
    key_wait = 2

file save:
    user.vim_call_rpc_function(":w", "command")

file editor exit:
    user.vim_call_rpc_function(":q", "command")

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

center that:
    user.vim_escape_insert_keys("h z")

chip:
    edit.undo()

pour that:
    user.vim_send_rpc_keys("<Esc>o")

mark [<user.letter>]:
    mark_name = letter or "a"
    user.vim_escape_insert_keys("m {mark_name}")

insert:
    user.vim_insert_mode()

trip move up: user.vim_escape_insert_keys("ctrl-f")
trip move down: user.vim_escape_insert_keys("ctrl-s")

# Would be better to use call RPC, but haven't worked out how
comp: user.vim_send_rpc_keys("<C-e>")
comp last: user.vim_send_rpc_keys("<C-p>")

format split toggle: user.vim_call_rpc_function(",m", "normal")

# Movement and editing, primarily anchored to line numbers.

jump mark [<user.letter>]:
    mark_name = letter or "a"
    user.vim_escape_insert_keys("` {mark_name}")

jump crown:
    user.vim_call_rpc_function("gg", "normal!")

jump foot:
    user.vim_call_rpc_function("G", "normal!")

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

change trip:
    # Using call_rpc doesn't preserve indentation
    user.vim_send_rpc_keys("<Esc>rr")

change {user.vim_text_object}:
    user.vim_call_rpc_function("d{vim_text_object}", "normal")
    user.vim_call_rpc_function("startinsert", "command")

chuck trip:
    user.vim_call_rpc_function("dd", "normal!")

chuck that:
    user.vim_call_rpc_function("d", "normal!")

chuck {user.vim_text_object}:
    user.vim_call_rpc_function("d{vim_text_object}", "normal")

take trip:
    user.vim_visual_line_mode()

take {user.vim_text_object}:
    user.vim_call_rpc_function("a{vim_text_object}", "normal")

take <user.vim_line_range>:
    user.vim_take_line_range(vim_line_range)

bring <user.vim_bring_range>:
    user.vim_bring(vim_bring_range)

pull:
    edit.copy()
    user.vim_go_mark("z")
    edit.paste()

comment that:
    user.vim_call_rpc_function(",cc", "normal")

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
# * Vim helper that show tokens nearby to the current cursor position so you don't have to say them. Though maybe this is a crutch for stack not working as well as hoped.
