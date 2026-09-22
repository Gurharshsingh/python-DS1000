# Assignment: Library Management REST API

## 1. Overview
In this assignment, you will build a backend REST API for a **Library Management System** using **FastAPI** and **Pydantic**. Your API will manage book records, library members, search queries, and book borrowing/returning workflows using in-memory data structures.

---

## 2. General Guidelines
Please review the following guidelines before starting:

1. **Pydantic Models**:
   - Define data schemas using Pydantic models for structured requests and responses.
2. **Response Format**:
   - Return either the requested data model or a Python dictionary with informative messages (such as `{"message": "..."}` or `{"error": "..."}`).
3. **Data Persistence**:
   - Store all data in-memory during application runtime (e.g., using Python lists or dictionaries).
4. **Interactive Documentation**:
   - Ensure your FastAPI application can be run with Uvicorn and tested via the interactive documentation at `/docs`.

---

## 3. Data Schema Requirements

Define the following Pydantic models:

### 3.1 `Book`
| Field Name | Type | Description | Default Value |
| :--- | :--- | :--- | :--- |
| `id` | `int` | Unique identifier for the book | *Required* |
| `title` | `str` | Title of the book | *Required* |
| `author` | `str` | Author of the book | *Required* |
| `genre` | `str` | Category/Genre (e.g., Fiction, Tech, Science) | *Required* |
| `is_available` | `bool` | Availability flag for borrowing | `True` |

### 3.2 `Member`
| Field Name | Type | Description | Default Value |
| :--- | :--- | :--- | :--- |
| `id` | `int` | Unique identifier for the member | *Required* |
| `name` | `str` | Full name of the library member | *Required* |
| `email` | `str` | Email address of the member | *Required* |

### 3.3 `BorrowRequest`
| Field Name | Type | Description | Default Value |
| :--- | :--- | :--- | :--- |
| `book_id` | `int` | ID of the book to be borrowed | *Required* |
| `member_id` | `int` | ID of the member borrowing the book | *Required* |

---

## 4. API Specification & Endpoints

### 4.1 General Endpoints
* **`GET /`**
  * **Description**: Root welcome endpoint.
  * **Expected Response**: `{"message": "Welcome to the Library Management API"}`

---

### 4.2 Member Management Endpoints
* **`POST /members`**
  * **Description**: Register a new library member.
  * **Request Body**: `Member` model.
  * **Expected Response**: The created member data.

* **`GET /members`**
  * **Description**: Retrieve all registered library members.
  * **Expected Response**: A list containing all member records.

---

### 4.3 Book Catalog Management (CRUD)
* **`POST /books`**
  * **Description**: Add a new book to the library catalog.
  * **Request Body**: `Book` model.
  * **Expected Response**: The newly added book data.

* **`GET /books`**
  * **Description**: Retrieve all books currently in the catalog.
  * **Expected Response**: A list containing all book records.

* **`GET /books/{book_id}`**
  * **Description**: Retrieve a specific book by its ID.
  * **Path Parameter**: `book_id` (`int`)
  * **Expected Response on Success**: The matching book record.
  * **Expected Response on Failure**: `{"error": "Book not found"}`

* **`PUT /books/{book_id}`**
  * **Description**: Update an existing book's information.
  * **Path Parameter**: `book_id` (`int`)
  * **Request Body**: `Book` model with updated details.
  * **Expected Response on Success**: The updated book record.
  * **Expected Response on Failure**: `{"error": "Book not found"}`

* **`DELETE /books/{book_id}`**
  * **Description**: Remove a book from the catalog.
  * **Path Parameter**: `book_id` (`int`)
  * **Expected Response on Success**: `{"message": "Book deleted successfully"}`
  * **Expected Response on Failure**: `{"error": "Book not found"}`

---

### 4.4 Search & Filtering (Query Parameters)
* **`GET /books/search`**
  * **Description**: Search and filter books by genre and availability.
  * **Query Parameters**:
    * `genre` (`str`, optional): Filter books that match this genre.
    * `available_only` (`bool`, optional, default: `False`): When `True`, return only books where `is_available` is `True`.
  * **Expected Response**: A list of matching book records.
  * *Note: Ensure endpoint route order in FastAPI prevents conflicts with the path parameter route `/books/{book_id}`.*

---

### 4.5 Borrowing & Returning Operations
* **`POST /borrow`**
  * **Description**: Process a book loan to a registered member.
  * **Request Body**: `BorrowRequest` model.
  * **Validation Rules**:
    1. Check if the book exists in the catalog. If not, return `{"error": "Book not found"}`.
    2. Check if the member exists in the members list. If not, return `{"error": "Member not found"}`.
    3. Check if the book is currently available (`is_available` is `True`). If not, return `{"error": "Book is currently unavailable"}`.
  * **Action**: Update the book's `is_available` attribute to `False`.
  * **Expected Response on Success**: 
    ```json
    {
      "message": "Book borrowed successfully",
      "book_id": 1,
      "member_id": 101
    }
    ```

* **`POST /return/{book_id}`**
  * **Description**: Process the return of a borrowed book.
  * **Path Parameter**: `book_id` (`int`)
  * **Validation Rules**:
    1. Check if the book exists in the catalog. If not, return `{"error": "Book not found"}`.
    2. Check if the book was borrowed. If `is_available` is already `True`, return `{"error": "Book was not borrowed"}`.
  * **Action**: Update the book's `is_available` attribute back to `True`.
  * **Expected Response on Success**: `{"message": "Book returned successfully"}`

---

## 5. Testing & Verification Checklist
Before submitting your work, make sure to test the following:
- [ ] Application starts up without errors using `uvicorn <filename>:app --reload`.
- [ ] All routes are visible and interactive in Swagger UI (`/docs`).
- [ ] Adding, viewing, updating, and deleting books works as expected.
- [ ] Adding and viewing members works as expected.
- [ ] Searching with query parameters correctly filters the books list.
- [ ] Borrowing updates the book's availability and handles invalid/unavailable cases.
- [ ] Returning a book resets its availability to available.
