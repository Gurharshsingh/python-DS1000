from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title = "Library Management")





class BookBase(BaseModel):
    title:str
    author:str
    price:float
    avaliable:bool=True


class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass


class BookResponse(BookBase):
    id : int
    created_at : datetime
    updated_at : datetime


books_db : dict[int,dict] = {

    1 : {
        'title' : 'The Great Gatsby',
        'author' : 'F. Scott Fitzgerald',
        'price' : 10.99,
        'avaliable' : True,
        'id' : 1,
        'created_at' : datetime.now(),
        'updated_at' : datetime.now()
    },

    2 : {
        'title' : 'To Kill a Mockingbird',
        'author' : 'Harper Lee',
        'price' : 12.99,
        'avaliable' : True,
        'id' : 2,
        'created_at' : datetime.now(),
        'updated_at' : datetime.now()
    },

    3 : {
        'title' : '1984',
        'author' : 'George Orwell',
        'price' : 14.99,
        'avaliable' : True,
        'id' : 3,
        'created_at' : datetime.now(),
        'updated_at' : datetime.now()
    }
}

next_book_id = 4

@app.get('/')
def read_root():
    return {'message' : 'Welcome to the Library Management System'}


@app.post('/books/', response_model = BookResponse, status_code = 201)
def create_book(book : BookCreate):
    now = datetime.now()
    global next_book_id
    new_book = book.model_dump()
    new_book['id'] = next_book_id
    new_book['created_at'] = now
    new_book['updated_at'] = now

    books_db[next_book_id] = new_book
    next_book_id += 1
    return new_book


@app.get("/books")
def get_all_books():
    return list(books_db.values())


@app.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    book = books_db.get(book_id)
    if book is None:
        return {'error' : 'Book not found'}
    return book


@app.put("/books/{book_id}")
def update_book(book_id : int , book : BookUpdate):
    if book_id not in books_db:
        return {'error' : 'Book not found'}
    
    update_book = book.model_dump()
    books_db[book_id].update(update_book)
    books_db[book_id]['updated_at'] = datetime.now()
    return books_db[book_id]



@app.delete("/books/{book_id}")
def delete_book(book_id : int):
    if book_id not in books_db:
        return {'error' : 'Book not found'}
    del books_db[book_id]
    return {'message' : 'Book deleted successfully'}
