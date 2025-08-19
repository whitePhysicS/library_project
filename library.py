from pydantic import BaseModel, Field, ValidationError
from dataclasses import dataclass, field
from typing import List, Optional, Literal
from pathlib import Path
from external import OpenLibraryClient
import json


class Book:
    def __init__(self, title: str, author: str, isbn: str, page_count):
        
        try:
            self.page_count = int(page_count)
        except Exception:
            self.page_count = page_count  
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False

    def borrow_book(self):
        if not self.is_borrowed:
            self.is_borrowed = True
        else:
            raise ValueError(f"'{self.title}' is already borrowed.")

    def return_book(self):
        if self.is_borrowed:
            self.is_borrowed = False
        else:
            raise ValueError(f"'{self.title}' was not borrowed.")

    def display_info(self) -> str:
        return f"'{self.title}' by {self.author} - {self.page_count} pages."
    
    def __str__(self) -> str:
        return self.display_info()

class EBook(Book):
    def __init__(self, title: str, author: str, isbn: str, file_format: str, page_count):
        super().__init__(title, author, isbn, page_count)
        self.file_format = file_format

    def display_info(self) -> str:
        return f"{super().display_info()} [Format: {self.file_format}]"
    
    def __str__(self) -> str:
        return self.display_info()

class AudioBook(Book):
    def __init__(self, title: str, author: str, isbn: str, duration_in_minutes: int, page_count):
        super().__init__(title, author, isbn, page_count)
        self.duration = int(duration_in_minutes)

    def display_info(self) -> str:
        return f"{super().display_info()} [Duration: {self.duration} mins]"
    
    def __str__(self) -> str:
        return self.display_info()


class Library:
    def __init__(
        self,
        name: str,
        data_file: str = "library.json",
        members_file: str = "members.json",
        base_dir: Path | None = None
    ):
        self.name = name

        base = Path(base_dir) if base_dir else Path(__file__).resolve().parent
        data_p = Path(data_file)
        member_p = Path(members_file)

        
        self.data_file = data_p if data_p.is_absolute() else (base / data_p)
        self.members_file = member_p if member_p.is_absolute() else (base / member_p)

       
        self._books: List[Book] = []
        self._members: List[Member] = []

        self.load_books()
        self.load_members()

    def add_book(self, book: Book) -> None:
        
        if any(b.isbn == book.isbn for b in self._books):
            
            return
        self._books.append(book)
        self.save_books()

    def remove_book(self, isbn: str) -> bool:
       
        for i, b in enumerate(self._books):
            if b.isbn == isbn:
                self._books.pop(i)
                self.save_books()
                return True
        return False

    def find_book(self, title: str) -> Optional[Book]:
        for book in self._books:
            if book.title.lower() == title.lower():
                return book
        return None

    def find_book_by_isbn(self, isbn: str) -> Optional[Book]:
        for book in self._books:
            if book.isbn == isbn:
                return book
        return None

    def borrow_by_isbn(self, isbn:str) -> bool:
        book= self.find_book_by_isbn(isbn) if hasattr(self, "find_book_by_isbn") else None
        if book is None:
            for b in getattr(self, "_books", []):
                if b.isbn == isbn:
                    book = b
                    break
        if book is None:
            return False
        try:
            book.borrow_book()
            return True
        except ValueError:
            return False       # Zaten alınmışsa False diyoruz.
        
    def return_by_isbn(self, isbn:str) -> bool:
        book = None
        for b in getattr(self, "_books" , []):
            if b.isbn == isbn:
                book = b
                break
        if book is None:
            return False
        try:
            book.return_book()
            return True
        except ValueError:
            return False    # Zaten iade edilmişse False diyoruz.
    
    def borrow_for_member(self, member_id: int, isbn: str) -> bool:

        member = self.find_member_by_id(member_id)
        book = self.find_book_by_isbn(isbn)

        if member is None or book is None:
            return False
        if book.is_borrowed:
            return False
        
        try:
            book.borrow_book()
        except ValueError:
            return False
        
        member.borrowed_books.append(book)

        self.save_books()
        self.save_members()
        return True
        
    def return_for_member(self, member_id: int, isbn:str) -> bool:

        member = self.find_member_by_id(member_id)
        book = self.find_book_by_isbn(isbn)

        if member is None or book is None:
            return False
        
        idx = None
        for i, b in enumerate(member.borrowed_books):
            if b.isbn == isbn:
                idx = i
                break
            if idx is None:
                return False
            
        try:
            book.return_book()
        except ValueError:
            return False
        
        member.borrowed_books.pop(idx)

        self.save_books()
        self.save_members()
        return True
    

    def who_has_isbn(self, isbn:str) -> int | None:
        for m in self._members:
            for b in m.borrowed_books:
                if b.isbn == isbn:
                    return m.member_id
        return None

    def add_book_by_isbn(self, isbn: str, kind:Literal["book","ebook","audiobook"]="book",*,file_format: str = "EPUB",duration_in_minutes: int | None= None,) -> bool:
        from external import OpenLibraryClient
        client = OpenLibraryClient()
        meta = client.fetch_by_isbn(isbn)
        if not meta or not meta.get("title"):
            return False
        title = meta["title"]
        authors = meta.get("authors", ["Unknown"])
        author_str = ", ".join(authors)
        page_count = meta.get("page_count") or 0

        if kind == "ebook":
            book = EBook(title,author_str, isbn, file_format, page_count)
        elif kind == "audiobook":
            duration = int(duration_in_minutes or 0)
            book = AudioBook(title, author_str, isbn, duration, page_count)
        else:
            book = Book(title, author_str, isbn, page_count)

        
        self.add_book(book)
        return True
            
    def list_books(self) -> list[Book]:
        return list(getattr(self, "_books", []))

    @property
    def total_books(self) -> int:
        return len(self._books)

    
    def save_books(self) -> None:
        
        payload = []
        for b in self._books:
            if isinstance(b, EBook):
                item_type = "EBook"
                payload.append({
                    "type": item_type,
                    "title": b.title,
                    "author": b.author,
                    "isbn": b.isbn,
                    "page_count": b.page_count,
                    "file_format": b.file_format,
                    "is_borrowed": b.is_borrowed,
                })
            elif isinstance(b, AudioBook):
                item_type = "AudioBook"
                payload.append({
                    "type": item_type,
                    "title": b.title,
                    "author": b.author,
                    "isbn": b.isbn,
                    "page_count": b.page_count,
                    "duration": b.duration,
                    "is_borrowed": b.is_borrowed,
                })
            else:
                item_type = "Book"
                payload.append({
                    "type": item_type,
                    "title": b.title,
                    "author": b.author,
                    "isbn": b.isbn,
                    "page_count": b.page_count,
                    "is_borrowed": b.is_borrowed,
                })

        
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.data_file.with_suffix(".json.tmp")
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        tmp_path.replace(self.data_file)


    def load_books(self) -> None:
        
        if not self.data_file.exists():
            return

        try:
            with self.data_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
        
            self._books = []
            return

        books: List[Book] = []
        for item in data:
            t = item.get("type", "Book")
            if t == "EBook":
                b = EBook(
                    title=item["title"],
                    author=item["author"],
                    isbn=item["isbn"],
                    file_format=item.get("file_format", "EPUB"),
                    page_count=item.get("page_count", 0),
                )
            elif t == "AudioBook":
                b = AudioBook(
                    title=item["title"],
                    author=item["author"],
                    isbn=item["isbn"],
                    duration_in_minutes=item.get("duration", 0),
                    page_count=item.get("page_count", 0),
                )
            else:
                b = Book(
                    title=item["title"],
                    author=item["author"],
                    isbn=item["isbn"],
                    page_count=item.get("page_count", 0),
                )
            
            b.is_borrowed = bool(item.get("is_borrowed", False))
            books.append(b)

        self._books = books

    def add_member(self, member: "Member") -> bool:
        if any(m.member_id == member.member_id for m in self._members):
            return False
        self._members.append(member)
        self.save_members()
        return True

    def list_members(self) -> List["Member"]:
        return list(self._members)

    def find_member_by_id(self, member_id: int) -> "Member | None":
        for m in self._members:
            if m.member_id == member_id:
                return m
        return None

    def save_members(self) -> None:
        payload = []
        for m in self._members:
            payload.append({
                "name": m.name,
                "member_id": m.member_id,
                "borrowed_isbns": [b.isbn for b in getattr(m, "borrowed_books", [])],
            })
        self.members_file.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.members_file.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        tmp.replace(self.members_file)

    def load_members(self) -> None:
        if not self.members_file.exists():
            return
        try:
            with self.members_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            self._members = []
            return

        members: List[Member] = []
        for item in data:
            m = Member(name=item["name"], member_id=int(item["member_id"]))
            borrowed = []
            for isbn in item.get("borrowed_isbns", []):
                b = self.find_book_by_isbn(isbn)
                if b is not None:
                    borrowed.append(b)
            m.borrowed_books = borrowed
            members.append(m)
        self._members = members

    def remove_member(self, member_id: int) -> bool:
        for i, m in enumerate(self._members):
            if m.member_id == member_id:
                self._members.pop(i)
                self.save_members()
                return True
        return False


@dataclass
class Member:
    name: str
    member_id: int
    borrowed_books: List[Book] = field(default_factory=list)

class PydanticBook(BaseModel):
    title: str
    author: str
    isbn: str = Field(..., min_length=10, max_length=13)
    publication_year: int = Field(..., gt=1400)

