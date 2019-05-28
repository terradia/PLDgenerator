import asana
from WebHook import *
from threading import Thread
from time import sleep


class AsanaSprint:
    def __init__(self, token):
        """

        @param token:
        @param task_id:
        """
        self.access_token = token
        self.client = asana.Client.access_token(self.access_token)
        self.json_pld = {}
        """self.webhook_manager = WebHookView(self)
        self.webhook_manager.register(app)
        thread = Thread(target=self._init_sprint_webhooks)
        thread.start()
        app.run(port="8080")"""

    def _init_sprint_webhooks(self):
        sleep(5)
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
            #dump(sprint)
            if not self._check_webhook(sprint["gid"]):
                self._post_webhook(sprint["gid"])

    def _check_webhook(self, sprint_gid):
        workspace_gid = self.client.get('/workspaces/', "")[0]["gid"]
        webhook = self.client.get(path='/webhooks/',
                                  query={"workspace": workspace_gid, "resource": sprint_gid})
        dump(webhook)
        #self.client.delete('/webhooks/' + webhook[0]["gid"], "")
        if len(webhook) == 0:
            print("webhook not set")
            return False
        print("webhook is set")
        return True

    def _post_webhook(self, task_id):
        """
        @return:
        """
        self.client.webhooks.create(resource=task_id, target="https://df8fc1bd.ngrok.io/WebHook")
        return self

    def get_sprint_tasks(self, tasks_ids):
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
        return self.json_pld
