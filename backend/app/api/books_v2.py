from fastapi import APIRouter, Body
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()

class Book:
    def __init__(self, id: int, title: str, author: str,description:str, category: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.category = category
        self.rating = rating

BOOKS =[
    Book(1, "Title one", "Author one", "Description one", "science", 5),
    Book(2, "Title two", "Author two", "Description two", "science", 4),
    Book(3, "Title three", "Author three", "Description three", "history", 3),
    Book(4, "Title four", "Author four", "Description four", "math", 5),
    Book(5, "Title five", "Author five", "Description five", "math", 4),
    Book(6, "Title six", "Author two", "Description six", "math", 3),
]

# Pydantic model for validated book input
class ValidatedBook(BaseModel):
    id: Optional[int] = Field(description="ID not needed as it will be computed automatically", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=5)
    description: str = Field(min_length=10, max_length=100)
    category: str
    rating: int = Field(gt=0, lt=6)
    
    # Provide an example for the JSON schema in the OpenAPI documentation
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Example Title",
                "author": "Example Author",
                "description": "Example Description",
                "category": "Example Category",
                "rating": 5
            }
        }
    }
    
    

@router.get("/books")
def get_all_books():
    return {"books": BOOKS}

# query parameters
# requestformat: http://localhost:8000/books/books?category=math
@router.get("/books/category")
def get_book_category(category: str):
    filtered_books = [book for book in BOOKS if book.category.casefold() == category.casefold()]
    return {"books": filtered_books}


# @router.post("/insert-book")
# def insert_book(book=Body()):
#     BOOKS.append(book)

@router.post("/insert-book")
def insert_book(book: ValidatedBook):
    # use ** to expand the dictionary key-values into keyword arguments for the Book constructor
    # this way I can create a Book instance from the validated Pydantic model
    new_book = Book(**book.dict())
    BOOKS.append(compute_book_id(new_book))
    
def compute_book_id(book: Book):
    # book.id = max([b.id for b in BOOKS], default=0) + 1
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@router.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    b = [book for book in BOOKS if book.id == book_id]
    return b


@router.put("/books/update_book")
def update_book(book: ValidatedBook):
    for index, current_book in enumerate(BOOKS):
        if current_book.id == book.id:
            BOOKS[index] = Book(**book.dict())