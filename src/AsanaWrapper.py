"""
    This module provide a wrapper to get information from asana
"""
import asana


class AsanaWrapper:
    """
        This class is wrapper used to get sprint information from asana
    """
    def __init__(self, token):
        """
        Create the Asana client object
        Setup the webhooks
        @param token: The access token used to authenticate to Asana
        """
        self.access_token = token
        self.client = asana.Client.access_token(self.access_token)
        self.json_pld = {}
        """self.webhook_manager = WebHookView(self)
        self.webhook_manager.register(app)
        thread = Thread(target=self._init_sprint_webhooks)
        thread.start()
        app.run(port="8080")"""

    def init_sprint_webhooks(self):
        """
        Get the sprint section's gid use it to request all Sprint's subtasks and post a webhook on each if the webhook
        doesn't exist
        """
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
            if not self._check_webhook(sprint["gid"]):
                self._post_webhook(sprint["gid"])

    def _check_webhook(self, sprint_gid):
        """
        Check if a webhook is attached to the specified gid passed by the sprint_gid param
        @param sprint_gid: the sprint gid
        @return: False if the webhook is not set, True if it is
        """
        workspace_gid = self.client.get('/workspaces/', "")[0]["gid"]
        webhook = self.client.get(path='/webhooks/',
                                  query={"workspace": workspace_gid, "resource": sprint_gid})
        #self.client.delete('/webhooks/' + webhook[0]["gid"], "")
        if not webhook:
            print("webhook not set")
            return False
        print("webhook is set")
        return True

    def _post_webhook(self, task_id):
        """
        Post a webhook on the tasks specified by the task_id param
        @param task_id: the tasks id related to where the webhook must be posted
        """
        self.client.webhooks.create(resource=task_id, target="https://df8fc1bd.ngrok.io/WebHook")

    def get_sprint_tasks(self, tasks_ids):
        """
        Loop through each task id passed as the tasks_ids array parameter and request all subtasks to create nested
        dictionary and lists that represent all the content of the sprint in this format:
        Sprint name 1:
        {
            Deliverable 1:
            {
                Card 1:
                [
                    task 1
                    Task 2
                ]
                Card 2:
                [
                    task 1
                ]
            }
        }

        @param tasks_ids:
        @return: the completed dictionary
        """
        print(tasks_ids)
        for task_id in tasks_ids:
            tasks = self.client.get("/tasks/" + str(task_id) + "/subtasks", "")
            for deliverable in tasks:
                card = self.client.get("/tasks/" + deliverable["gid"] + "/subtasks", "")
                cards = {}
                print("deliverable: ", deliverable["name"])
                for tabs in card:
                    tab = self.client.get("/tasks/" + tabs["gid"] + "/subtasks", "")
                    subs = []
                    for sub in tab:
                        done = bool(self.client.get("/tasks/" + sub["gid"], "")["completed"])
                        subs.append({"storie": sub["name"], "done": done})
                    cards[tabs["name"]] = subs
                self.json_pld[deliverable["name"]] = cards
        return self.json_pld
