"""
server.py
----------
Flask backend for the custom-built MovieFlix frontend.

Reuses recommender.py (unchanged) — this file's only job is to expose
that logic as JSON endpoints for our own HTML/CSS/JS to call.

Endpoints:
  GET /                          -> serves the custom frontend (index.html)
  GET /api/titles                -> list of all movie titles (for search box)
  GET /api/genres                -> list of all genres (for genre pills)
  GET /api/similar?title=...     -> content-based recommendations
  GET /api/top-rated             -> popularity-ranked movies
  GET /api/genre?name=...        -> movies in a given genre
"""

from flask import Flask, jsonify, request, render_template
from recommender import MovieRecommender

app = Flask(__name__)
engine = None


def get_engine():
    global engine
    if engine is None:
        engine = MovieRecommender("movie.csv", "rating.csv")
    return engine


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/titles")
def titles():
    return jsonify(get_engine().all_titles())


@app.route("/api/genres")
def genres():
    return jsonify(get_engine().all_genres())


@app.route("/api/similar")
def similar():
    title = request.args.get("title", "")
    n = int(request.args.get("n", 12))
    df = get_engine().recommend_similar(title, top_n=n)
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/top-rated")
def top_rated():
    n = int(request.args.get("n", 12))
    df = get_engine().top_rated(top_n=n)
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/genre")
def by_genre():
    name = request.args.get("name", "")
    n = int(request.args.get("n", 12))
    df = get_engine().by_genre(name, top_n=n)
    return jsonify(df.to_dict(orient="records"))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)