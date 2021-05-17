title: /Google Chrome$/
-
tag(): user.tabs
tab select:
    user.telector_show("active_window:0 2 -40 30", "explicit_colors:#8b8e92 #b5b7bc #dde0e5 #dde1e5 #dde1e6 #dee0e6 #dee1e5 #dee1e6 #dee2e7 #dfe1e6 #dfe1e7 #dfe2e7 #e1e4e8 #e5e8ec #e6e8ec #e8eaed #eef0f2 #eff0f2 #eff1f3 #f1f3f5 #f2f3f5 #f7f8f9 #f8f9fa #fbfbfc #fbfcfc #fcfdfd #ffffff")

action(app.tab_next): key(ctrl-pagedown)
action(app.tab_previous): key(ctrl-pageup)
