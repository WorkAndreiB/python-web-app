from fastapi import APIRouter, Body

router = APIRouter()

BOOKS =[
    {"title": "Title one", "author": "Author one", "category": "science"},
    {"title": "Title two", "author": "Author two", "category": "science"},
    {"title": "Title three", "author": "Author three", "category": "history"},
    {"title": "Title four", "author": "Author four", "category": "math"},
    {"title": "Title five", "author": "Author five", "category": "math"},
    {"title": "Title six", "author": "Author two", "category": "math"},
]


@router.get("/books")
def get_all_books():
    return {"books": BOOKS}

# query parameters
# requestformat: http://localhost:8000/books/books?category=math
@router.get("/books/category")
def get_book_category(category: str):
    filtered_books = [book for book in BOOKS if book["category"].casefold() == category.casefold()]
    return {"books": filtered_books}


# path parameters 
# request format: http://localhost:8000/books/books/Title%20one
@router.get("/books/{book_title}")
def get_book_by_title(book_title: str):
    filtered_books = [book for book in BOOKS if book["title"].casefold() == book_title.casefold()]
    return {"books": filtered_books}


# path parameter with optional query parameter
# request format: http://localhost:8000/books/books/author/Author%20two?category=math
@router.get("/books/{book_author}")
def get_book_by_author(book_author: str, category: str = None):
    books = []
    
    for book in BOOKS:
        if (book["author"].casefold() == book_author.casefold()) and \
                (category is None or book["category"].casefold() == category.casefold()):
            books.append(book)
    return {"books": books}


# create a new book entry
# request format: http://localhost:8000/books/create_book
# request body format: {"title": "Title seven", "author": "Author seven", "category": "science"}
@router.post("/books/create_book")
def create_book(new_book = Body()):
    BOOKS.append(new_book)
    return {"message": "Book created successfully", "book": new_book}


# update an existing book entry
# request format: http://localhost:8000/books/update_book/Title%20one
# request body format: {"title": "Title one", "author": "Author one", "category": "science"}
@router.put("/books/update_book/{book_title}")
def update_book(book_title: str, updated_book = Body()):
    for index, book in enumerate(BOOKS):
        if book["title"].casefold() == book_title.casefold():
            BOOKS[index] = updated_book
            return {"message": "Book updated successfully", "book": updated_book}
    return {"message": "Book not found"}


# delete an existing book entry
# request format: http://localhost:8000/books/delete_book/Title%20one
# request body is not required for delete operation
@router.delete("/books/delete_book/{book_title}")
def delete_book(book_title: str):
    for index, book in enumerate(BOOKS): 
        if book.get("title", "").casefold() == book_title.casefold():
            del BOOKS[index]
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}

