import asana
from dump import *
import json
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer


class AsanaSprint:
    def __init__(self, token, task_id):
        """

        @param token:
        @param task_id:
        """
        self.access_token = token
        self.client = asana.Client.access_token(self.access_token)
        self.main_sprint_task_id = ""
        self.sprint_task_id = ""
        self.json_pld = {}
        self._webhook()

    def _sprint_update_handler(self, r, *args, **kwargs):
        pass

    def _run_server(self):
        """

        @return:
        """
        custom_webhook = MakeWebhook(self)
        server = HTTPServer(('localhost', 8080), custom_webhook)
        server.serve_forever()


    def _webhook(self):
        """
        @return:
        """
        print("_webhook()")
        thread = Thread(target=self._run_server, args=())
        thread.start()
        print("server thread started")
        response = self.client.post(path="/webhooks/", data={"resource": "",
                                                             "target": ""})
        dump(response)
        return self

    def get_sprint_tasks(self):
        print("get_sprint_tasks()")
        """

        @param sprint_task_id:
        """
        tasks = self.client.get("/tasks/" + self.sprint_task_id + "/subtasks", "")
        for deliverable in tasks:
            card = self.client.get("/tasks/" + deliverable["gid"] + "/subtasks", "")
            cards = {}
            print("deliverable: ", deliverable["name"])
            for tabs in card:
                tab = self.client.get("/tasks/" + tabs["gid"] + "/subtasks", "")
                subs = []
                for sub in tab:
                    subs.append(sub["name"])
                cards[tabs["name"]] = subs
            self.json_pld[deliverable["name"]] = cards
        dump(self.json_pld)


def MakeWebhook(client):
    class WebHook(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.client = client
            super(WebHook, self).__init__(*args, **kwargs)

        def do_POST(self):
            print(json.dumps(json.loads(self.rfile.read(int(self.headers.get('content-length')))), indent=4))
            self.send_response(200)
            print(int(self.headers.get('content-length')))
            if int(self.headers.get('content-length')) == 2:
                print("send Secret")
                self.send_header("X-Hook-Secret", self.headers.get("X-Hook-Secret"))
            else:
                print("change triggerd")
                self.client.sprint_task_id = ""
                self.client.get_sprint_tasks()
            self.end_headers()
    return WebHook

