title: /^VIM.+\.shoppinglist/
title: /shoppinglist - Visual Studio Code$/
-
add [<number_small> unit] [<user.shopping_list_quantity>] <phrase>:
    count = number_small or "1"
    quantity = user.shopping_list_quantity or ""
    insert("{count} x {quantity}{phrase}")
    key(enter)
