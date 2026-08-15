# MovieFlix — Netflix-style Movie Recommendation System
## (Custom HTML/CSS/JS frontend + Flask backend — no Streamlit)

## 1. Setup (VS Code terminal)

```bash
cd path/to/this/folder
pip install -r requirements.txt
```

## 2. Add your real dataset

Your Kaggle "MovieLens 20M" download contains files like `movie.csv` and
`rating.csv` (or `movies.csv` / `ratings.csv`). Copy **just those two
files** into this folder, replacing the small sample ones.

- If your files are named `movies.csv` / `ratings.csv` (with the "s"),
  either rename them, OR open `server.py` and change this line to match:
  ```python
  engine = MovieRecommender("movie.csv", "rating.csv")
  ```
- The full 20M-row ratings file can take ~30-60s to load. For a smoother
  live demo, trim it once beforehand:
  ```python
  import pandas as pd
  pd.read_csv("rating.csv", nrows=2_000_000).to_csv("rating.csv", index=False)
  ```

## 3. Run it

```bash
python server.py
```

Then open **http://127.0.0.1:5000** in your browser. Leave the terminal
running during your presentation.

## 4. Project structure (this IS your custom frontend)

```
server.py            <- Flask backend: exposes recommender.py as JSON APIs
recommender.py       <- all the ML/logic (unchanged, no UI code)
templates/index.html <- the page structure
static/style.css     <- Netflix-style dark theme, card rows, hover effects
static/script.js     <- fetches data from the Flask API and renders cards
```

No frontend framework, no template library beyond Flask's built-in
Jinja (`render_template`) — this is a hand-built HTML/CSS/JS frontend
talking to a Python backend over a JSON API, a standard real-world
architecture and easy to explain if asked "how does the frontend talk
to the backend?": the JS calls endpoints like `/api/similar?title=...`
with `fetch()`, gets JSON back, and injects movie cards into the page.

## 5. What's actually happening (for your presentation)

- **`recommender.py`** — the ML engine:
  - **Content-based filtering**: genre strings → vectors (`CountVectorizer`)
    → `cosine_similarity` finds movies closest in genre to one you like.
    Powers "Because you watched X".
  - **Popularity ranking**: a Bayesian average per movie from
    `rating.csv`, blending the movie's own average with the overall
    average, weighted by number of ratings — so a movie with 3 ratings
    can't outrank one with 10,000. Powers "Top Rated".
  - **Genre browsing**: filters movies whose genre string contains the
    selected genre.
- **`server.py`** — four small JSON endpoints, one per feature, plus `/`
  which serves the page itself.
- **`static/script.js`** — on page load, fetches the movie title list
  (for the search box), the genre list (for the dropdown), and the
  top-rated row. On search or genre change, it calls the matching
  endpoint and re-renders that row's cards.

If asked "is this collaborative filtering?" — be precise: it's a
**hybrid**. Similarity is content-based (genres only). Ranking uses
real ratings data, which leans collaborative but isn't full user-user /
item-item collaborative filtering (no rating-matrix factorization).
That's a fair, honest scope for a beginner project, and a clean answer
if asked about future work (e.g. the `surprise` library's SVD).

## 6. If something breaks right before your presentation

- Browser shows nothing / blank cards → open browser dev tools (F12) →
  Console tab, check for a red error, and tell me exactly what it says.
- `FileNotFoundError` in the terminal → your CSVs aren't named/placed
  correctly, see step 2.
- `KeyError` about a column → your Kaggle CSV has different column
  names; send me the exact header row from your CSV and I'll patch
  `recommender.py` in one line.
- Page loads but data never appears → the Flask server terminal will
  show any Python error live; paste it here.
