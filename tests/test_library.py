#python -m pytest -v

import pytest
from library import Book


def test_book_creation():
        book = Book("The Hobbit", "J.R.R. Tolkien", "978-0345339683", "319")
        assert book.title == "The Hobbit"
        assert book.author == "J.R.R. Tolkien"
        assert book.is_borrowed == False

def test_borrow_and_return_logic():      
    book = Book("Dune", "Frank Herbert", "978-0441013593", "319") 
    book.borrow_book()   
    assert book.is_borrowed == True    
    book.return_book()  
    assert book.is_borrowed == False