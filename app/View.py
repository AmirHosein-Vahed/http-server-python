from typing import Optional
from Response import Response
from Request import Request
import os

class View:
    """View handlers for different HTTP endpoints."""
    
    @staticmethod
    def index(req: Request, res: Response) -> None:
        """Handle the root path ('/') endpoint."""
        res.set_status(200)

    @staticmethod
    def user_agent(req: Request, res: Response) -> None:
        """
        Handle the '/user-agent' endpoint.
        Returns the User-Agent header from the request.
        """
        res.set_status(200)
        req.set_user_agent()
        res.add_header({"Content-Type": "text/plain"})
        res.add_header({"Content-Length": str(len(req.user_agent))})
        res.set_body(req.user_agent)

    @staticmethod
    def get_file(req: Request, res: Response) -> None:
        """
        Handle GET requests to '/files/...' endpoint.
        Serves files from the static directory.
        """
        file_name = req.URLpath.split("/")[2]
        file_path = os.path.join(res.static_dir, file_name) if res.static_dir else None

        if not file_path or not os.path.isfile(file_path):
            res.set_status(404)
            return

        try:
            with open(file_path, 'rb') as file:
                content = file.read()

            res.set_status(200)
            res.add_header({"Content-Type": "application/octet-stream"})
            res.add_header({"Content-Length": str(os.path.getsize(file_path))})
            res.set_body(content.decode())
        except Exception as e:
            res.set_status(500)
            res.set_body(f"Error reading file: {str(e)}")

    @staticmethod
    def post_file(req: Request, res: Response) -> None:
        """
        Handle POST requests to '/files/...' endpoint.
        Saves files to the static directory.
        """
        file_name = req.URLpath.split("/")[2]
        
        if not res.static_dir or not os.path.isdir(res.static_dir):
            res.set_status(404)
            return

        try:
            file_path = os.path.join(res.static_dir, file_name)
            with open(file_path, 'w') as file:
                file.write(req.body)
            res.set_status(201)
        except Exception as e:
            res.set_status(500)
            res.set_body(f"Error writing file: {str(e)}")

    @staticmethod
    def serve(req: Request, res: Response) -> None:
        """
        Handle GET requests to '/serve/...' endpoint.
        Serves HTML files from the static directory.
        """
        file_name = req.URLpath.split("/")[2]
        file_path = os.path.join(res.static_dir, file_name) if res.static_dir else None

        if not file_path or not os.path.isfile(file_path):
            res.set_status(404)
            return

        try:
            with open(file_path, 'rb') as file:
                content = file.read()

            res.set_status(200)
            res.add_header({"Content-Type": "text/html"})
            res.add_header({"Content-Length": str(os.path.getsize(file_path))})
            res.set_body(content.decode())
        except Exception as e:
            res.set_status(500)
            res.set_body(f"Error reading file: {str(e)}")

    @staticmethod
    def echo(req: Request, res: Response) -> None:
        """
        Handle GET requests to '/echo/...' endpoint.
        Returns the path parameter as plain text.
        """
        arg = req.URLpath.split("/")[2]
        res.set_status(200)
        res.add_header({"Content-Type": "text/plain"})
        res.add_header({"Content-Length": str(len(arg))})
        res.set_body(arg)