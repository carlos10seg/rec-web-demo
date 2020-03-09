from flask import Flask, render_template, jsonify, request
from controller import Controller
application = Flask(__name__)
 
@application.route("/")
def index():
    return render_template('index.html')

@application.route("/recs", methods=['POST'])
def get_recs():
    users = list(map(int, request.form.get("users").split(',')))
    nr_recs = request.form.get("nrrecs")
    algo = request.form.get("algo")
    items = list(map(int, request.form.get("items").split(',')))
    ctrl = Controller()
    return jsonify({"result": ctrl.get_recs(users, nr_recs, algo, items)})

@application.route("/movies")
def get_movies():
    term = str.lower(request.args.get('term', ''))
    movies = []
    if len(term) > 0:
        ctrl = Controller()
        movies = ctrl.get_movies(term)
    return jsonify({"result": movies})
    
if __name__ == "__main__":
    application.run()