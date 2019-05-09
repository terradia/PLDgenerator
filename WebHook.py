import json
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from dump import *


class WebHook(BaseHTTPRequestHandler):
    def __init__(self, client, *args, **kwargs):
        self.client = client
        super(WebHook, self).__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get('content-length'))))
        dump(body)
        self.send_response(200)
        print(int(self.headers.get('content-length')))
        if int(self.headers.get('content-length')) == 2:
            print("send Secret")
            self.send_header("X-Hook-Secret", self.headers.get("X-Hook-Secret"))
        else:
            print("change triggerd")
            if len(body["events"]) != 0:
                tasks_ids = set()
                for event in body["events"]:
                    tasks_ids.add(event["resource"])
                self.client.get_sprint_tasks(tasks_ids)
        self.end_headers()


