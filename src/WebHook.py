from flask import Flask, request, Response
from flask_classful import FlaskView, route

app = Flask(__name__)


class WebHookView(FlaskView):
    def __init__(self, client):
        print("WebHook: __init__()")
        self.client = client

    @route("/", methods=["POST"])
    def _webhook_update(self):
        # self.asana.get_sprint_tasks("")
        print("_webhook_update()")
        print(request.get_json())
        data = request.get_json()
        if len(data["events"]) == 0:
            print("sending X-Hook-Secret: ", request.headers["X-Hook-Secret"])
            return Response(status=200, headers={"X-Hook-Secret": request.headers["X-Hook-Secret"]})
        print("change triggered")
        return Response(status=200)
