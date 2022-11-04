'''
Server code and full application flow.
'''

import arc_feedback, distribute
from flask import Flask, request, render_template
import csv, datetime, os
from log import print

# constants
NUM_JUDGES = 20
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

print("Starting server ======================", important=True)
print("Initializing Flask app")
app = Flask(__name__)
print("Time is", datetime.datetime.now())

# load entries from csv
with open(os.path.join(THIS_FOLDER, 'data/entries.csv'), newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    entries = list(reader)
print("Detected Entries ======================", important=True)
for j in [", ".join(i) for i in entries]:
    print(j)

# distribute entries
assignments = distribute.distribute(entries, NUM_JUDGES)
rankings = {}
full_ranking = []
top_5_exact = []
rankings_graph = []

print("Awaiting responses ======================", important=True)

@app.route('/rank/<id>', methods=["GET", "POST"])
def rank_view(id):
    global rankings, full_ranking, top_5_exact, rankings_graph
    if request.method == "GET":
        return render_template("rank.html", projects = assignments[int(id)])
    elif request.method == "POST":
        # Retrieve and store rankings
        order = request.get_json()["order"]
        print(f"Received ranking from judge {id}: {order}", important=True)
        rankings[id] = order

        print("Calculating preliminary full rankings")
        
        # Calculate rankings
        rankings_graph = {}
        for judge in rankings.values():
            for i, project1 in enumerate(judge):
                if project1 not in rankings_graph:
                    rankings_graph[project1] = {}
                for project2 in judge[i+1:]:
                    if project2 not in rankings_graph[project1]:
                        rankings_graph[project1][project2] = 0
                    rankings_graph[project1][project2] += 1
        print(rankings_graph)
        
        full_ranking = arc_feedback.approx_ranking(rankings_graph)
        print("Full ranking (approximate):", full_ranking)

        return '{"status":"Success!"}'

@app.route('/log')
def log_view():
    log = open("log.txt", "r").read()
    return render_template("log.html", log=log)

@app.route('/', methods=["GET", "POST"])
def index_view():
    global top_5_exact, full_ranking, rankings, rankings_graph
    if request.method == "POST":
        if len(full_ranking) > 0:
            # calculate exact mfas
            top_5 = full_ranking[:5]
            exact_fas_input = {}
            for i in top_5:
                exact_fas_input[i[0]] = {
                    j : rankings_graph[i[0]][j]
                    for j in rankings_graph[i[0]].keys()
                    if j in [
                        k[0] for k in top_5
                    ]
                }
            print("Exact FAS input:", exact_fas_input)
            top_5_exact = arc_feedback.exact_fas(exact_fas_input)
            print("Top 5 exact:", top_5_exact)

    total = NUM_JUDGES
    print(full_ranking)
    awaiting = [i for i in range(total) if str(i) not in rankings.keys()]
    return render_template("index.html", total=total, awaiting=awaiting, ranking=full_ranking, top5=top_5_exact)

if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)