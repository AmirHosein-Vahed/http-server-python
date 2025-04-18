from typing import List, Tuple, Callable
from View import View
from Request import Request
from Response import Response


# Type alias for route definitions
Route = Tuple[str, str, Callable[[Request, Response], None]]

# Define all routes in the application
router_map: List[Route] = [
    ("GET", "/", View.index),
    ("GET", "/user-agent", View.user_agent),
    ("GET", "^/files/", View.get_file),
    ("POST", "^/files/", View.post_file),
    ("GET", "^/echo/", View.echo),
    ("GET", "^/serve/", View.serve),
]