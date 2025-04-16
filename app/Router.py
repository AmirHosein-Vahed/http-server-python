from View import View

router_map = [
    ("GET",  "/"          , View.index),
    ("GET",  "/user-agent", View.user_agent),
    ("GET",  "^/files/"   , View.get_file),
    ("POST", "^/files/"   , View.post_file),
    ("GET",  "^/echo/"    , View.echo),
]