from talon import Context, registry, app


ctx = Context()
ctx.matches = r"""
os: linux
"""

def _add_keys():
    """
    Put this in a launch listener so it runs after knausj
    """

    # Add return as a first class alias for enter
    my_special_key_list = {
        k: v
        for k, v in registry.lists['user.special_key'][0].items()
    }
    my_special_key_list['enta'] = 'enter'
    ctx.lists['self.special_key'] = my_special_key_list

    my_symbol_key_list = {
        k: v
        for k, v in registry.lists['user.symbol_key'][0].items()
    }
    my_symbol_key_list['semi'] = ';'
    ctx.lists['self.symbol_key'] = my_symbol_key_list

    my_punctuation_key_list = {
        k: v
        for k, v in registry.lists['user.punctuation'][0].items()
    }
    my_punctuation_key_list['semi'] = ';'
    ctx.lists['self.punctuation'] = my_punctuation_key_list

app.register("launch", _add_keys)
