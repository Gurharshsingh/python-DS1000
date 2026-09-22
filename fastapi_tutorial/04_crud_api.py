"""
=============================================================
 FastAPI Tutorial - Chapter 4: Full CRUD REST API
=============================================================
 TOPICS COVERED:
   1. Complete CRUD (Create, Read, Update, Delete)
   2. Proper REST API design
   3. Partial updates with PATCH
   4. In-memory database simulation
   5. Best practices

 HOW TO RUN:
   >>> uvicorn 04_crud_api:app --reload --port 8003

 THEN VISIT:
   - http://127.0.0.1:8003/docs  → Full API documentation

 CRUD = Create → POST
        Read   → GET
        Update → PUT (full) / PATCH (partial)
        Delete → DELETE
=============================================================
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="📚 Library Management API",
    description="""
    A complete CRUD REST API for managing a library.
    
    ## Features
    - 📖 Manage books (CRUD)
    - 👤 Manage members (CRUD)
    - 🔍 Search and filter
    
    This is a teaching example of proper REST API design.
    """,
    version="4.0.0"
)


# ==============================================================
# 📌 DATA MODELS
# ==============================================================

class BookBase(BaseModel):
    """Fields shared between input and output models."""
    title: str
    author: str
    isbn: str
    price: float
    genre: str = "Fiction"
    available: bool = True


class BookCreate(BookBase):
    """Model for creating a new book (input)."""
    pass


class BookUpdate(BookBase):
    """Model for full update (PUT) - all fields required."""
    pass


class BookPartialUpdate(BaseModel):
    """Model for partial update (PATCH) - all fields optional."""
    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    price: float | None = None
    genre: str | None = None
    available: bool | None = None


class BookResponse(BookBase):
    """Model for the response (output) - includes server-generated fields."""
    id: int
    created_at: datetime
    updated_at: datetime


# ==============================================================
# 📌 IN-MEMORY DATABASE
# ==============================================================

books_db: dict[int, dict] = {
    1: {
        "id": 1,
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "isbn": "9781593279288",
        "price": 39.99,
        "genre": "Programming",
        "available": True,
        "created_at": datetime(2024, 1, 1),
        "updated_at": datetime(2024, 1, 1),
    },
    2: {
        "id": 2,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "price": 45.99,
        "genre": "Programming",
        "available": True,
        "created_at": datetime(2024, 1, 2),
        "updated_at": datetime(2024, 1, 2),
    },
    3: {
        "id": 3,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "isbn": "9780062315007",
        "price": 14.99,
        "genre": "Fiction",
        "available": True,
        "created_at": datetime(2024, 1, 3),
        "updated_at": datetime(2024, 1, 3),
    },
}

next_book_id = 4  # Next available ID


def find_book_or_404(book_id: int) -> dict:
    """Helper function to get a book or raise 404."""
    if book_id not in books_db:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id={book_id} not found."
        )
    return books_db[book_id]


# ==============================================================
# 📌 CRUD ENDPOINTS
# ==============================================================

# ── CREATE ──────────────────────────────────────────────────

@app.post(
    "/books",
    response_model=BookResponse,
    status_code=201
)
def create_book(book: BookCreate):
    """
    **Create a new book** in the library.
    
    - **title**: Book title (required)
    - **author**: Author name (required)  
    - **isbn**: ISBN-10 or ISBN-13 (required)
    - **price**: Price in USD > 0 (required)
    - **genre**: Book genre (default: Fiction)
    - **available**: Is the book available? (default: True)
    """
    global next_book_id
    
    # Check for duplicate ISBN
    for existing in books_db.values():
        if existing["isbn"] == book.isbn:
            raise HTTPException(
                status_code=409,
                detail=f"Book with ISBN '{book.isbn}' already exists."
            )
    
    now = datetime.now()
    new_book = {
        "id": next_book_id,
        **book.model_dump(),         # Unpack all fields from the model
        "created_at": now,
        "updated_at": now,
    }
    books_db[next_book_id] = new_book
    next_book_id += 1
    return new_book


# ── READ (list) ──────────────────────────────────────────────

@app.get(
    "/books",
    response_model=list[BookResponse],
    summary="Get all books",
    tags=["Books"]
)
def get_all_books(
    genre: str | None = None,
    available: bool | None = None,
    skip: int = 0,
    limit: int = 10
):
    """
    **Get all books** with optional filtering and pagination.
    
    - Filter by **genre** (e.g., ?genre=Programming)
    - Filter by **available** status (e.g., ?available=true)
    - Use **skip** and **limit** for pagination
    """
    books = list(books_db.values())
    
    # Apply filters
    if genre:
        books = [b for b in books if b["genre"].lower() == genre.lower()]
    if available is not None:
        books = [b for b in books if b["available"] == available]
    
    # Paginate
    total = len(books)
    books = books[skip: skip + limit]
    
    return books


# ── READ (single) ────────────────────────────────────────────

@app.get(
    "/books/{book_id}",
    response_model=BookResponse,
    summary="Get a single book",
    tags=["Books"]
)
def get_book(book_id: int):
    """
    **Get a single book** by its ID.
    
    Returns 404 if the book is not found.
    """
    return find_book_or_404(book_id)


# ── UPDATE (full) ─────────────────────────────────────────────

@app.put(
    "/books/{book_id}",
    response_model=BookResponse,
    summary="Fully update a book (PUT)",
    tags=["Books"]
)
def update_book(book_id: int, book: BookUpdate):
    """
    **Fully update a book** (PUT).
    
    PUT replaces the **entire resource** - all fields must be provided.
    If you only want to update some fields, use PATCH instead.
    """
    existing = find_book_or_404(book_id)
    updated_book = {
        "id": book_id,
        **book.model_dump(),
        "created_at": existing["created_at"],  # Keep original creation time
        "updated_at": datetime.now(),
    }
    books_db[book_id] = updated_book
    return updated_book


# ── UPDATE (partial) ─────────────────────────────────────────

@app.patch(
    "/books/{book_id}",
    response_model=BookResponse,
    summary="Partially update a book (PATCH)",
    tags=["Books"]
)
def partial_update_book(book_id: int, book_update: BookPartialUpdate):
    """
    **Partially update a book** (PATCH).
    
    PATCH updates **only the provided fields**.
    Unspecified fields keep their current values.
    
    Example: Only update the price:
    ```json
    { "price": 29.99 }
    ```
    """
    existing = find_book_or_404(book_id)
    
    # model_dump(exclude_unset=True) only includes fields the client actually sent
    update_data = book_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update."
        )
    
    # Merge existing data with new data
    updated_book = {**existing, **update_data, "updated_at": datetime.now()}
    books_db[book_id] = updated_book
    return updated_book


# ── DELETE ──────────────────────────────────────────────────

@app.delete(
    "/books/{book_id}",
    status_code=204,
    summary="Delete a book",
    tags=["Books"]
)
def delete_book(book_id: int):
    """
    **Delete a book** by ID.
    
    Returns 204 No Content on success.
    Returns 404 if book not found.
    """
    find_book_or_404(book_id)
    del books_db[book_id]
    return None


# ── SEARCH ──────────────────────────────────────────────────

@app.get(
    "/books/search/",
    response_model=list[BookResponse],
    summary="Search books",
    tags=["Books"]
)
def search_books(q: str):
    """
    **Search books** by title or author name.
    
    Case-insensitive search across title and author.
    Example: /books/search/?q=python
    """
    q = q.lower()
    results = [
        book for book in books_db.values()
        if q in book["title"].lower() or q in book["author"].lower()
    ]
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No books found matching '{q}'"
        )
    return results


# ── STATS ───────────────────────────────────────────────────

@app.get("/stats", tags=["Stats"])
def get_library_stats():
    """Get statistics about the library."""
    books = list(books_db.values())
    genres = {}
    for book in books:
        genres[book["genre"]] = genres.get(book["genre"], 0) + 1
    
    return {
        "total_books": len(books),
        "available_books": sum(1 for b in books if b["available"]),
        "unavailable_books": sum(1 for b in books if not b["available"]),
        "genres": genres,
        "average_price": round(sum(b["price"] for b in books) / len(books), 2) if books else 0,
    }
