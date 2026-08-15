"""
recommender.py
----------------
Core recommendation logic. Two techniques, combined:

1. CONTENT-BASED FILTERING
   Every movie's genre string ("Action|Sci-Fi|Thriller") is turned into a
   vector using CountVectorizer, then we use cosine similarity to find
   movies whose genre-vectors are closest to a movie you already like.
   -> Answers: "Because you watched X, here's something similar."

2. POPULARITY / RATINGS SIGNAL
   We use rating.csv to compute each movie's average rating and number of
   ratings (a "Bayesian average" so a movie with 2 five-star ratings
   doesn't beat a movie with 5000 ratings averaging 4.3).
   -> Answers: "Trending Now" / "Top Rated" rows, just like Netflix's
      homepage rows.

Combining both is exactly the idea behind real hybrid recommender systems,
and it's simple enough to explain confidently in a viva/presentation.
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, movies_path="movie.csv", ratings_path="rating.csv"):
        self.movies = pd.read_csv(movies_path)
        self.ratings = pd.read_csv(ratings_path)

        # normalize column names in case Kaggle version differs slightly
        self.movies.columns = [c.strip().lower() for c in self.movies.columns]
        self.ratings.columns = [c.strip().lower() for c in self.ratings.columns]

        self.movies["genres"] = self.movies["genres"].fillna("")
        self.movies["genres_clean"] = self.movies["genres"].str.replace("|", " ", regex=False)

        self._build_content_model()
        self._build_popularity_scores()

    # ---------- 1. CONTENT-BASED MODEL ----------
    def _build_content_model(self):
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split())
        genre_matrix = vectorizer.fit_transform(self.movies["genres_clean"])
        self.similarity_matrix = cosine_similarity(genre_matrix)
        self.title_to_index = pd.Series(
            self.movies.index, index=self.movies["title"]
        ).drop_duplicates()

    def recommend_similar(self, title, top_n=10):
        """Content-based: movies similar in genre to `title`."""
        if title not in self.title_to_index:
            return pd.DataFrame()
        idx = self.title_to_index[title]
        scores = list(enumerate(self.similarity_matrix[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        scores = [s for s in scores if s[0] != idx][:top_n]
        movie_indices = [i[0] for i in scores]
        return self.movies.iloc[movie_indices][["movieid", "title", "genres"]]

    # ---------- 2. POPULARITY MODEL ----------
    def _build_popularity_scores(self):
        stats = self.ratings.groupby("movieid")["rating"].agg(["mean", "count"])
        C = stats["mean"].mean()          # overall average rating
        m = stats["count"].quantile(0.60)  # minimum votes threshold

        def bayesian_avg(row):
            v, R = row["count"], row["mean"]
            return (v / (v + m)) * R + (m / (v + m)) * C

        stats["score"] = stats.apply(bayesian_avg, axis=1)
        self.popularity = stats.sort_values("score", ascending=False)

    def top_rated(self, top_n=10):
        merged = self.popularity.merge(
            self.movies, left_index=True, right_on="movieid"
        )
        return merged[["movieid", "title", "genres", "score"]].head(top_n)

    # ---------- 3. BROWSE BY GENRE ----------
    def by_genre(self, genre, top_n=10):
        matches = self.movies[self.movies["genres"].str.contains(genre, case=False, na=False)]
        return matches[["movieid", "title", "genres"]].head(top_n)

    def all_genres(self):
        genre_set = set()
        for g in self.movies["genres"]:
            genre_set.update(g.split("|"))
        genre_set.discard("(no genres listed)")
        return sorted(genre_set)

    def all_titles(self):
        return sorted(self.movies["title"].tolist())
