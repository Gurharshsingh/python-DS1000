"""
=============================================================
 Practice Exercise: Based on Chapters 1 & 2
=============================================================
 Domain: Movie Database API
 
 This file combines concepts from 01_hello_world.py and 
 02_pydantic_models.py into a completely new domain!

 FEATURES INCLUDED:
   - FastAPI application instance
   - Path & Query Parameters (from Chapter 1)
   - Pydantic Models & Nested Models (from Chapter 2)
   - Request & Response Models (from Chapter 2)
   - Basic CRUD Operations (POST, GET, PUT, DELETE)

 HOW TO RUN:
   >>> uvicorn practice_test:app --reload --port 8002
=============================================================
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Movie Database Practice API",
    description="A practice project combining FastAPI routing and Pydantic models.",
    version="1.0.0"
)

# ==============================================================
# Pydantic Models
# ==============================================================

class Director(BaseModel):
    """Nested model representing a director."""
    name: str
    nationality: str


class MovieInput(BaseModel):
    """Model for receiving movie data (Request Body)."""
    title: str
    release_year: int
    genre: str
    director: Director  # Nested Pydantic model!
    internal_notes: str | None = None  # Sensitive/Internal field


class MovieOutput(BaseModel):
    """Model for returning movie data (Response Body)."""
    id: int
    title: str
    release_year: int
    genre: str
    director: Director
    # Notice: 'internal_notes' is excluded from output for security!


# Fake In-Memory Database
movies_db = {}
next_movie_id = 1


# ==============================================================
# Endpoints
# ==============================================================

@app.get("/")
def welcome():
    """Root endpoint (Chapter 1)"""
    return {"message": "Welcome to the Movie Database API 🎬"}


@app.post("/movies", response_model=MovieOutput, status_code=201)
def create_movie(movie: MovieInput):
    """
    Create a new movie using Pydantic models. (Chapter 2)
    Returns MovieOutput to hide 'internal_notes'.
    """
    global next_movie_id
    movie_dict = movie.model_dump()
    
    new_movie = {
        "id": next_movie_id,
        "title": movie_dict["title"],
        "release_year": movie_dict["release_year"],
        "genre": movie_dict["genre"],
        "director": movie_dict["director"],
        "internal_notes": movie_dict.get("internal_notes")
    }
    
    movies_db[next_movie_id] = new_movie
    next_movie_id += 1
    
    return new_movie


@app.get("/movies")
def get_movies(genre: str = "all", limit: int = 10):
    """
    Get movies with optional query parameters (Chapter 1).
    Example: /movies?genre=Sci-Fi&limit=5
    """
    results = list(movies_db.values())
    
    if genre.lower() != "all":
        results = [m for m in results if m["genre"].lower() == genre.lower()]
        
    return {
        "count": len(results[:limit]), 
        "movies": results[:limit]
    }


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    """
    Get a specific movie by its path parameter ID (Chapter 1).
    """
    if movie_id not in movies_db:
        return {"error": "Movie not found"}
    return movies_db[movie_id]


@app.put("/movies/{movie_id}", response_model=MovieOutput)
def update_movie(movie_id: int, movie: MovieInput):
    """
    Update a movie completely (Chapter 2).
    """
    if movie_id not in movies_db:
        return {"error": "Movie not found"}
        
    movie_dict = movie.model_dump()
    updated_movie = {
        "id": movie_id,
        "title": movie_dict["title"],
        "release_year": movie_dict["release_year"],
        "genre": movie_dict["genre"],
        "director": movie_dict["director"],
        "internal_notes": movie_dict.get("internal_notes")
    }
    
    movies_db[movie_id] = updated_movie
    return updated_movie


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    """
    Delete a movie by ID (Chapter 2).
    """
    if movie_id not in movies_db:
        return {"error": "Movie not found"}
        
    deleted = movies_db.pop(movie_id)
    return {"message": "Movie deleted successfully", "deleted": deleted}
