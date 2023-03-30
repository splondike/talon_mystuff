from urllib.parse import quote_plus

from talon import Context, actions

ctx = Context()
ctx.matches = "app: firefox"

@ctx.action("user.search_with_search_engine")
def search_with_search_engine(search_template: str, search_text: str):
    url = search_template.replace("%s", quote_plus(search_text))
    actions.app.tab_open()
    actions.insert(url)
    actions.key("enter")
