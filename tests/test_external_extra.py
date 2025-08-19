import pytest

def test_add_book_by_isbn_not_found(monkeypatch, tmp_path):
    from library import Library
    lib = Library("TestLib", base_dir=tmp_path)

    # OpenLibrary client None döndürsün (404 benzeri).
    class DummyClient:
        def fetch_by_isbn(self, isbn): 
            return None

    import external
    monkeypatch.setattr(external, "OpenLibraryClient", lambda *a, **kw: DummyClient())

    ok = lib.add_book_by_isbn("0000000000")
    assert ok is False

def test_add_book_by_isbn_success(monkeypatch, tmp_path):
    from library import Library
    lib = Library("TestLib", base_dir=tmp_path)

    class DummyClient:
        def fetch_by_isbn(self, isbn):
            return {
                "title": "Clean Code",
                "authors": ["Robert C. Martin"],
                "page_count": 464
            }

    import external
    monkeypatch.setattr(external, "OpenLibraryClient", lambda *a, **kw: DummyClient())

    ok = lib.add_book_by_isbn("9780132350884")
    assert ok is True

    # Gerçekten kaydedildi mi? kaydedilmedi mi?
    books = lib.list_books()
    isbns = [b.isbn for b in books]
    assert "9780132350884" in isbns
