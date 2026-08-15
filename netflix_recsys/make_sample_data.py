"""
Generates a small SAMPLE dataset with the exact same columns as the real
MovieLens 20M Kaggle dataset, just so we can test the app end-to-end
before you plug in your real movie.csv / rating.csv.
"""
import pandas as pd
import numpy as np

movies = pd.DataFrame({
    "movieId": range(1, 21),
    "title": [
        "Toy Story (1995)", "Jumanji (1995)", "Heat (1995)", "Se7en (1995)",
        "The Usual Suspects (1995)", "Braveheart (1995)", "Apollo 13 (1995)",
        "The Lion King (1994)", "Pulp Fiction (1994)", "Forrest Gump (1994)",
        "The Shawshank Redemption (1994)", "Speed (1994)", "Interstellar (2014)",
        "The Dark Knight (2008)", "Inception (2010)", "The Matrix (1999)",
        "Titanic (1997)", "Finding Nemo (2003)", "Gladiator (2000)", "Shrek (2001)"
    ],
    "genres": [
        "Adventure|Animation|Children|Comedy|Fantasy", "Adventure|Children|Fantasy",
        "Action|Crime|Thriller", "Mystery|Thriller", "Crime|Mystery|Thriller",
        "Action|Drama|War", "Adventure|Drama|IMAX", "Animation|Children|Drama|Musical",
        "Comedy|Crime|Drama", "Comedy|Drama|Romance", "Crime|Drama",
        "Action|Romance|Thriller", "Adventure|Drama|Sci-Fi", "Action|Crime|Drama",
        "Action|Sci-Fi|Thriller", "Action|Sci-Fi", "Drama|Romance",
        "Adventure|Animation|Children|Comedy", "Action|Adventure|Drama",
        "Adventure|Animation|Children|Comedy|Fantasy"
    ]
})
movies.to_csv("movie.csv", index=False)

np.random.seed(42)
n_ratings = 500
ratings = pd.DataFrame({
    "userId": np.random.randint(1, 40, n_ratings),
    "movieId": np.random.randint(1, 21, n_ratings),
    "rating": np.random.choice([0.5,1,1.5,2,2.5,3,3.5,4,4.5,5], n_ratings),
    "timestamp": 1000000000
})
ratings.to_csv("rating.csv", index=False)
print("Sample movie.csv and rating.csv created.")
