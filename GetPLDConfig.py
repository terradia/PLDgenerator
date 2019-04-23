import asana
from dump import *


personal_access_token = ''
client = asana.Client.access_token(personal_access_token)
diag = {}
PLD = client.get("/tasks//subtasks", "")
for deliverable in PLD:
    card = client.get("/tasks/" + deliverable["gid"] + "/subtasks", "")
    cards = {}
    print("deliverable: ", deliverable["name"])
    for tabs in card:
        tab = client.get("/tasks/" + tabs["gid"] + "/subtasks", "")
        subs = []
        for sub in tab:
            subs.append(sub["name"])
        cards[tabs["name"]] = subs
    diag[deliverable["name"]] = cards
dump(diag)
