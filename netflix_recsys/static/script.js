// TMDB API Setup
const TMDB_API_KEY = "85943b399c91bd802ee88fa0eb24042e"; // <-- PASTE YOUR KEY HERE
const TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500";
const DEFAULT_POSTER = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80";

// Comprehensive Dataset with Types, Genres, and Scores
const DATASET = [
    // Movies
    { title: "The Dark Knight", type: "Movie", genre: "Action", score: 98 },
    { title: "The Matrix", type: "Movie", genre: "Action", score: 94 },
    { title: "Avatar", type: "Movie", genre: "Action", score: 91 },
    { title: "Inception", type: "Movie", genre: "Sci-Fi", score: 97 },
    { title: "Interstellar", type: "Movie", genre: "Sci-Fi", score: 95 },
    { title: "Toy Story", type: "Movie", genre: "Animation", score: 98 },
    { title: "Pulp Fiction", type: "Movie", genre: "Thriller", score: 96 },
    { title: "Fight Club", type: "Movie", genre: "Drama", score: 93 },
    { title: "Forrest Gump", type: "Movie", genre: "Drama", score: 90 },
    { title: "The Conjuring", type: "Movie", genre: "Horror", score: 94 },
    { title: "La La Land", type: "Movie", genre: "Romance", score: 93 },
    
    // TV Shows
    { title: "Stranger Things", type: "TV Show", genre: "Sci-Fi", score: 97 },
    { title: "Dark", type: "TV Show", genre: "Sci-Fi", score: 94 },
    { title: "Breaking Bad", type: "TV Show", genre: "Drama", score: 99 },
    { title: "Wednesday", type: "TV Show", genre: "Horror", score: 92 },
    { title: "The Office", type: "TV Show", genre: "Comedy", score: 95 }
];

document.addEventListener("DOMContentLoaded", () => {
    loadTopRated();
    getRecommendations(); // Render initial row on page load
});

// Fetch poster dynamically from TMDB API
async function fetchPosterUrl(title) {
    if (!TMDB_API_KEY || TMDB_API_KEY === "YOUR_TMDB_API_KEY") {
        return DEFAULT_POSTER;
    }
    try {
        const response = await fetch(
            `https://api.themoviedb.org/3/search/multi?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(title)}`
        );
        const data = await response.json();
        if (data.results && data.results.length > 0 && data.results[0].poster_path) {
            return `${TMDB_IMAGE_BASE}${data.results[0].poster_path}`;
        }
    } catch (error) {
        console.error("Error fetching poster:", error);
    }
    return DEFAULT_POSTER;
}

// Render individual movie card with dynamic image loading
async function renderCard(title, matchPercent, container) {
    const card = document.createElement("div");
    card.className = "card";

    // Placeholder skeleton loading
    card.innerHTML = `
        <div style="width:100%; height:260px; background:#222; border-radius:6px; display:flex; align-items:center; justify-content:center; color:#555;">
            Loading poster...
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 10px;">
            <span style="color: #46d369; font-weight: 700; font-size: 0.9rem;">${matchPercent}% Match</span>
        </div>
        <div class="card-title">${title}</div>
    `;
    container.appendChild(card);

    // Fetch poster URL dynamically via TMDB API
    const posterUrl = await fetchPosterUrl(title);
    
    // Swap placeholder with actual image element
    const placeholder = card.querySelector("div");
    if (placeholder) {
        placeholder.outerHTML = `<img src="${posterUrl}" alt="${title}" onerror="this.src='${DEFAULT_POSTER}'">`;
    }
}

// Top Rated Section
async function loadTopRated() {
    const container = document.getElementById("topRatedRow");
    if (!container) return;
    container.innerHTML = "";
    
    const topMovies = [
        { title: "The Dark Knight", score: 98 },
        { title: "Inception", score: 95 },
        { title: "Pulp Fiction", score: 92 },
        { title: "The Matrix", score: 89 },
        { title: "Interstellar", score: 87 }
    ];

    for (const item of topMovies) {
        await renderCard(item.title, item.score, container);
    }
}

// Dynamic Search & Filter Logic
async function getRecommendations() {
    const inputTitle = document.getElementById("movieInput").value.trim().toLowerCase();
    const selectedType = document.getElementById("typeSelect").value;
    const selectedGenre = document.getElementById("genreSelect").value;
    
    let container = document.getElementById("genreRow");
    if (!container) return;

    container.innerHTML = "";

    // 1. Filter local dataset based on type, genre, and text search
    let filteredResults = DATASET.filter(item => {
        const matchesType = (selectedType === "All" || item.type === selectedType);
        const matchesGenre = (!selectedGenre || item.genre === selectedGenre);
        const matchesSearch = (!inputTitle || item.title.toLowerCase().includes(inputTitle));
        
        return matchesType && matchesGenre && matchesSearch;
    });

    // 2. If a custom search title is entered and not in local array, generate dynamic card
    if (inputTitle && filteredResults.length === 0) {
        const rawSearch = document.getElementById("movieInput").value.trim();
        filteredResults = [
            { title: rawSearch, score: 98 },
            { title: "Inception", score: 92 },
            { title: "The Matrix", score: 88 }
        ];
    } 
    // 3. Fallback to general list if specific filters yield no matches
    else if (filteredResults.length === 0) {
        filteredResults = DATASET.filter(item => (selectedType === "All" || item.type === selectedType)).slice(0, 4);
    }

    // Render cards sequentially with live posters
    for (const item of filteredResults) {
        await renderCard(item.title, item.score, container);
    }
}