from typing import List, Optional, Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from library import Library, Book, EBook, AudioBook, Member

app = FastAPI(title="Mew's Library API", version="1.0.0")
lib = Library(name="API Library", data_file="library.json", members_file="members.json")

class BookIn(BaseModel):
    title: str
    author: str
    isbn: str = Field(..., min_length=10)
    page_count: int = Field(0, ge=0)
    kind: Literal["book", "ebook", "audiobook"] = "book"
    file_format: Optional[str] = "EPUB"
    duration_in_minutes: Optional[int] = Field(default=None, ge=0)

class BookOut(BaseModel):
    title: str
    author: str
    isbn: str
    page_count: int
    type: str
    is_borrowed: bool

def to_out(b: Book) -> BookOut:
    t = "Book"
    if isinstance(b, EBook):
        t = "EBook"
    elif isinstance(b, AudioBook):
        t = "AudioBook"
    return BookOut(
        title=b.title,
        author=b.author,
        isbn=b.isbn,
        page_count=int(getattr(b, "page_count", 0) or 0),
        type=t,
        is_borrowed=bool(getattr(b, "is_borrowed", False)),
    )

class MemberIn(BaseModel):
    name: str
    member_id: int = Field(..., ge=1)

class MemberOut(BaseModel):
    name: str
    member_id: int
    borrowed: List[BookOut]

def member_to_out(m: Member) -> MemberOut:
    return MemberOut(
        name= m.name,
        member_id=m.member_id,
        borrowed=[to_out(b) for b in getattr(m, "borrowed_books", [])],
    )


# ==== BOOKS ====

@app.get("/books", response_model=List[BookOut])
def list_books():
    return [to_out(b) for b in lib.list_books()]

@app.get("/books/{isbn}", response_model=BookOut)
def get_book(isbn: str):
    b = lib.find_book_by_isbn(isbn)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    return to_out(b)

@app.post("/books", status_code=201, response_model=BookOut)
def add_book(body: BookIn):
    
    if lib.find_book_by_isbn(body.isbn):
        raise HTTPException(status_code=409, detail="ISBN already exists")

    if body.kind == "ebook":
        b = EBook(body.title, body.author, body.isbn, body.file_format or "EPUB", body.page_count)
    elif body.kind == "audiobook":
        b = AudioBook(body.title, body.author, body.isbn, int(body.duration_in_minutes or 0), body.page_count)
    else:
        b = Book(body.title, body.author, body.isbn, body.page_count)

    ok = lib.add_book(b) 
    if ok is False:
        raise HTTPException(status_code=409, detail="ISBN already exists")

    return to_out(b)

@app.post("/books/isbn/{isbn}", status_code=201, response_model=BookOut)
def add_book_by_isbn(isbn: str, kind: Literal["book","ebook","audiobook"]="book",
                     file_format: str="EPUB", duration_in_minutes: int=0):
    
    if lib.find_book_by_isbn(isbn):
        raise HTTPException(status_code=409, detail="ISBN already exists")

    ok = False
    if kind == "ebook":
        ok = lib.add_book_by_isbn(isbn, kind="ebook", file_format=file_format or "EPUB")
    elif kind == "audiobook":
        ok = lib.add_book_by_isbn(isbn, kind="audiobook", duration_in_minutes=int(duration_in_minutes or 0))
    else:
        ok = lib.add_book_by_isbn(isbn, kind="book")

    if not ok:
        raise HTTPException(status_code=404, detail="Book not found on OpenLibrary")

   
    b = lib.find_book_by_isbn(isbn)
    return to_out(b)

@app.delete("/books/{isbn}", status_code=204)
def delete_book(isbn: str):
    ok = lib.remove_book(isbn)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return None 

# ==== MEMBERS ====

@app.get("/members", response_model=List[MemberOut])
def list_members():
    return [member_to_out(m) for m in lib.list_members()]

@app.get("/members/{member_id}", response_model=MemberOut)
def get_member(member_id: int):
    m = lib.find_member_by_id(member_id)
    if not m:
        raise HTTPException(status_code=404, detail="Member not found")
    return member_to_out(m)

@app.post("/members", status_code=201, response_model=MemberOut)
def add_member(body: MemberIn):
    
    if lib.find_member_by_id(body.member_id):
        raise HTTPException(status_code=409, detail="Member ID already exists")

    ok = lib.add_member(Member(name=body.name, member_id=body.member_id))
    if not ok:
        
        raise HTTPException(status_code=409, detail="Member ID already exists")

    m = lib.find_member_by_id(body.member_id)
    return member_to_out(m)

@app.delete("/members/{member_id}", status_code=204)
def delete_member(member_id: int):
    
    if not hasattr(lib, "remove_member") or not lib.remove_member(member_id):
        raise HTTPException(status_code=404, detail="Member not found")
    return None

# === BORROW / RETURN for member ===

@app.post("/members/{member_id}/borrow/{isbn}", status_code=204)
def borrow_for_member(member_id: int, isbn: str):
    ok = lib.borrow_for_member(member_id, isbn)
    if not ok:
        
        raise HTTPException(
            status_code=400,
            detail="Cannot borrow (member/book not found or already borrowed)",
        )
    return None

@app.post("/members/{member_id}/return/{isbn}", status_code=204)
def return_for_member(member_id: int, isbn: str):
    ok = lib.return_for_member(member_id, isbn)
    if not ok:
        raise HTTPException(
            status_code=400,
            detail="Cannot return (member/book not found or member doesn't have this book)",
        )
    return None

