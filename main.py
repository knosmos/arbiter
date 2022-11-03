'''
Server code and full application flow.
'''

import arc_feedback, distribute, toposort
from flask import Flask, request, jsonify, render_template
import csv, datetime
from log import print

# constants
NUM_JUDGES = 20

print("Starting server ======================", important=True)
print("Initializing Flask app")
app = Flask(__name__)
print("Time is", datetime.datetime.now())

# load entries from csv
with open('data/entries.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    entries = list(reader)
print("Detected Entries ======================", important=True)
for j in [", ".join(i) for i in entries]:
    print(j)

# distribute entries
assignments = distribute.distribute(entries, NUM_JUDGES)
rankings = {}

print("Awaiting responses ======================", important=True)

@app.route('/rank/<id>', methods=["GET", "POST"])
def rank_view(id):
    if request.method == "GET":
        return render_template("rank.html", projects = assignments[int(id)])
    elif request.method == "POST":
        order = request.get_json()["order"]
        print(f"Received ranking from judge {id}: {order}")
        rankings[id] = order
        return '{"status":"Success!"}'

@app.route('/log')
def log_view():
    log = open("log.txt", "r").read()
    return render_template("log.html", log=log)

@app.route('/')
def index_view():
    total = NUM_JUDGES
    print(rankings)
    awaiting = [i for i in range(total) if str(i) not in rankings.keys()]
    return render_template("index.html", total=total, awaiting=awaiting)

if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)