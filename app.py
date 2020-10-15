from flask import Flask, render_template, jsonify, request
from controller import Controller
application = Flask(__name__)
 
@application.route("/")
def index():
    ctrl = Controller()
    user_id = ctrl.get_current_user_id()
    return render_template('index.html', value=user_id)

@application.route("/recs", methods=['POST'])
def get_recs():
    users = list(map(int, request.form.get("users").split(',')))
    nr_recs = request.form.get("nrrecs")
    algo = request.form.get("algo")
    items = request.form.get("items")
    ctrl = Controller()
    return jsonify({"result": ctrl.get_recs_from_recserver(users, nr_recs, algo, items)})


@application.route("/qprecs", methods=['POST'])
def get_qprecs():
    movies = list(map(int, request.form.get("movies").split(',')))
    nr_recs = request.form.get("nrrecs")
    items = request.form.get("items")
    algo = request.form.get("algo")
    user_id = request.form.get("user")
    ctrl = Controller()
    return jsonify({"result": ctrl.get_qprecs(algo, movies, nr_recs, items, user_id)})

@application.route("/movies")
def get_movies():
    term = str.lower(request.args.get('term', ''))
    movies = []
    if len(term) > 0:
        ctrl = Controller()
        movies = ctrl.get_movies(term)
    return jsonify({"result": movies})
    
@application.route("/imageurl")   
def get_image_url():
    movie_id = request.args.get('movie_id', '')
    ctrl = Controller()
    return jsonify({"image_url": ctrl.get_image_url(movie_id)})

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5002)