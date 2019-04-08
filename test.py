import asana
import sys


def dump(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        print('%s{' % ((nested_level) * spacing))
        for k, v in obj.items():
            if hasattr(v, '__iter__') and type(v) != str:
                print('%s%s:' % ((nested_level + 1) * spacing, k))
                dump(v, nested_level + 1, output)
            else:
                print('%s%s: %s' % ((nested_level + 1) * spacing, k, v))
        print('%s}' % (nested_level * spacing))
    elif type(obj) == list:
        print('%s[' % ((nested_level) * spacing))
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print('%s%s' % ((nested_level + 1) * spacing, v))
        print('%s]' % ((nested_level) * spacing))
    else:
        print('%s%s' % (nested_level * spacing, obj))

# replace with your personal access token.
personal_access_token = ''

# Construct an Asana client
client = asana.Client.access_token(personal_access_token)
# Set things up to send the name of this script to us to show that you succeeded! This is optional.
client.options['client_name'] = "hello_world_python"

# Get your user info
diag = {}
PLD = client.get("", "")
for deliverable in PLD:
    card = client.get("/tasks/" + deliverable["gid"] + "/subtasks", "")
    cards = {}
    for tabs in card:
        tab = client.get("/tasks/" + tabs["gid"] + "/subtasks", "")
        subs = []
        for sub in tab:
            subs.append(sub["name"])
        cards[tabs["name"]] = subs
    diag[deliverable["name"]] = cards
dump(diag)



