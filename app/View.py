from Response import Response
from Request import Request
import os

class View:
    def __init__(self):
        pass

    # "/"
    def index(req: Request, res: Response):
        res.set_status(200)

    # "/user-agent"
    def user_agent(req: Request, res: Response):
        res.set_status(200)
        req.set_user_agent()
        res.add_header({"Content-Type": "text/plain"})
        res.add_header({"Content-Length": len(req.user_agent)})
        res.set_body(req.user_agent)

    # "/files/..."
    def get_file(req: Request, res: Response):
        file_name = req.URLpath.split("/")[2]
        # print("File name ==", file_name)
        # print("Static dir ==", res.static_dir)
        # print("Is file? ==", os.path.isfile(os.path.join(res.static_dir, file_name)))

        if res.static_dir is None or not os.path.isfile(os.path.join(res.static_dir, file_name)):
            res.set_status(404)

        else:
            file_path = os.path.join(res.static_dir, file_name)
            # print("File path ::", file_path)
            with open(file_path) as file:
                content = file.read()

            res.set_status(200)
            res.add_header({"Content-Type": "application/octet-stream"})
            res.add_header({"Content-Length": os.path.getsize(file_path)})
            res.set_body(content)

    # "/files/..."
    def post_file(req: Request, res: Response):
        # req.print_data()
        file_name = req.URLpath.split("/")[2]

        if res.static_dir is None or not os.path.isdir(res.static_dir):
            res.set_status(404)

        else:
            with open(os.path.join(res.static_dir, file_name), 'w') as file:
                file.write(req.body)
            res.set_status(201)

    # "/echo/..."
    def echo(req: Request, res: Response):
        arg = req.URLpath.split("/")[2]
        res.set_status(200)
        res.add_header({"Content-Type": "text/plain"})
        res.add_header({"Content-Length": len(arg)})
        res.set_body(arg)