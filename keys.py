from talon import Context, registry


ctx = Context()
ctx.matches = r"""
os: linux
"""

# Add return as a first class alias for enter
my_list = {
    k: v
    for k, v in registry.lists['user.special_key'][0].items()
}
my_list['return'] = 'enter'
ctx.lists['self.special_key'] = my_list
