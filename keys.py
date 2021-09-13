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
    my_list = {
        k: v
        for k, v in registry.lists['user.special_key'][0].items()
    }
    my_list['return'] = 'enter'
    my_list['tabby'] = 'tab'
    ctx.lists['self.special_key'] = my_list
app.register("launch", _add_keys)
