#python -m pytest -v
from library import Library, Book
import json
from pathlib import Path

def test_add_find_remove(tmp_path):
    data_file = tmp_path / "library.json"
    lib = Library("TestLib", data_file=str(data_file))

    b = Book("Dune", "Frank Herbert", "978-0441013593", 412)
    lib.add_book(b)
    assert lib.total_books == 1

    found = lib.find_book("Dune")
    assert found is not None
    assert found.author == "Frank Herbert"

    ok = lib.remove_book("978-0441013593")
    assert ok is True
    assert lib.total_books == 0

def test_persistence(tmp_path):
    data_file = tmp_path / "library.json"
    lib1 = Library("TestLib", data_file=str(data_file))
    lib1.add_book(Book("1984", "George Orwell", "978-0451524935", 319))
    assert lib1.total_books == 1

    # yeni instance aynı dosyadan yükleyebilmeli
    lib2 = Library("TestLib", data_file=str(data_file))
    assert lib2.total_books == 1
    assert lib2.find_book("1984") is not None

def test_borrow_return_by_isbn(tmp_path):
    data_file = tmp_path / "library.json"
    lib = Library("TestLib", data_file=str(data_file))
    lib.add_book(Book("The Hobbit", "J.R.R. Tolkien", "978-0345339683", 319))

    assert lib.borrow_by_isbn("978-0345339683") is True
    # iki kez ödünç alma başarısız olmalı
    assert lib.borrow_by_isbn("978-0345339683") is False
    # iade
    assert lib.return_by_isbn("978-0345339683") is True
    # iki kez iade başarısız olmalı
    assert lib.return_by_isbn("978-0345339683") is False
