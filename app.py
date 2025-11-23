import os
import pickle
import requests
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

MOVIE_DICT_PATH = "artifacts/movie_dict.pkl"
SIMILARITY_PATH = "artifacts/similarity.pkl"

if not os.path.exists(MOVIE_DICT_PATH):
    raise FileNotFoundError(f"movie_dict.pkl not found at: {MOVIE_DICT_PATH}")

if not os.path.exists(SIMILARITY_PATH):
    raise FileNotFoundError(f"similarity.pkl not found at: {SIMILARITY_PATH}")

movies_dict = pickle.load(open(MOVIE_DICT_PATH, "rb"))
movies = pd.DataFrame(movies_dict)

movies["title_stripped"] = movies["title"].astype(str).str.strip()
movies["title_lower"] = movies["title_stripped"].str.lower()

similarity = pickle.load(open(SIMILARITY_PATH, "rb"))

TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        data = requests.get(url, timeout=5).json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w185{poster_path}"
    except Exception:
        pass
    return "https://placehold.co/185x278/333/FFFFFF?text=No+Poster"

def recommend(movie_title):
    movie_title = str(movie_title).strip()
    try:
        idx = movies[movies["title_stripped"] == movie_title].index[0]
    except Exception:
        return [], [], [], []

    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    names, posters, years, ratings = [], [], [], []

    for i, _ in distances[1:25]:
        row = movies.iloc[i]
        names.append(row.title)
        posters.append(fetch_poster(row.movie_id))
        years.append(row.get("year", "—"))
        ratings.append(row.get("vote_average", "—"))

    return names, posters, years, ratings

def find_suggestions(query, limit=8):
    q = str(query).strip().lower()
    if not q:
        return []

    matches = movies[movies["title_lower"].str.contains(q, na=False)].head(limit)
    suggestions = []

    for _, row in matches.iterrows():
        suggestions.append({
            "title": row.get("title_stripped"),
            "poster": fetch_poster(row.get("movie_id")),
            "year": row.get("year", "—"),
            "rating": row.get("vote_average", "—")
        })

    return suggestions

@app.route("/", methods=["GET", "POST"])
def home():
    suggestions = []
    recommendations = []
    all_movies = movies["title_stripped"].tolist()

    if request.method == "POST":
        movie = request.form.get("movie", "").strip()

        if movie.lower() not in movies["title_lower"].values:
            suggestions = find_suggestions(movie, limit=8)
        else:
            names, posters, years, ratings = recommend(movie)
            recommendations = [
                {"title": n, "poster": p, "year": y, "rating": r}
                for n, p, y, r in zip(names, posters, years, ratings)
            ]

    return render_template(
        "index.html",
        recommendations=recommendations,
        all_movies=all_movies,
        suggestions=suggestions
    )

if __name__ == "__main__":
    app.run(debug=True)
