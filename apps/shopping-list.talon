title: /^VIM.+\.shoppinglist/
title: /shoppinglist - Visual Studio Code$/
-
add [<number_small> unit] [<user.shopping_list_quantity>] <user.shopping_list_phrase>:
    count = number_small or "1"
    quantity = user.shopping_list_quantity or ""
    insert("{count} x {quantity}{shopping_list_phrase}")
    key(enter)
