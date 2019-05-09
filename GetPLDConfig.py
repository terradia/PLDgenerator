import asana
from dump import *
from WebHook import *
from functools import partial


class AsanaSprint:
    def __init__(self, token):
        """

        @param token:
        @param task_id:
        """
        self.access_token = token
        self.client = asana.Client.access_token(self.access_token)
        self.json_pld = {}
        thread = Thread(target=self._run_server, args=())
        thread.start()
        self._init_sprint_webhooks()

    def _run_server(self):
        """

        @return:
        """
        custom_webhook = partial(WebHook, self)
        server = HTTPServer(('localhost', 8080), custom_webhook)
        server.serve_forever()

    def _init_sprint_webhooks(self):
        print("_init_sprint_webhooks()")
        project = self.client.get("/projects/", "")[0]["gid"]
        sections = self.client.get("/projects/" + project + "/sections/", "")
        sprint_gid = ""
        for section in sections:
            if section["name"] == "Sprint":
                sprint_gid = section["gid"]
                break
        if sprint_gid == "":
            print("sprint section can not be found")
            return
        sprints = self.client.get("/sections/" + sprint_gid + "/tasks/", "")
        for sprint in sprints:
            dump(sprint)
            if not self._check_webhook(sprint["gid"]):
                self._post_webhook(sprint["gid"])

    def _check_webhook(self, sprint_gid):
        workspace_gid = self.client.get('/workspaces/', "")[0]["gid"]
        webhook = self.client.get(path='/webhooks/',
                                  query={"workspace": workspace_gid, "resource": sprint_gid})
        if len(webhook) == 0:
            print("webhook not set")
            return False
        print("webhook is set")
        return True

    def _post_webhook(self, task_id):
        """
        @return:
        """
        print("_post_webhook()")
        self.client.webhooks.create(resource=task_id, target="")
        return self

    def get_sprint_tasks(self, tasks_ids):
        print("get_sprint_tasks()")
        """

        @param sprint_task_id:
        """
        print(tasks_ids)
        for task_id in tasks_ids:
            try:
                tasks = self.client.get("/tasks/" + str(task_id) + "/subtasks", "")
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
            except:
                pass
            dump(self.json_pld)
