from fastapi.testclient import TestClient

def test_books_api_flow(tmp_path, monkeypatch):
  
    from api import app
    from library import Library

  
    import api as api_mod
    api_mod.lib = Library(name="Test API Library", base_dir=tmp_path)

    client = TestClient(app)


    r = client.get("/books")
    assert r.status_code in (200,204)
    assert r.json() == []
 
    # Normal kitap ekleme testi.
    r = client.post("/books", json={
        "title": "Test Book",
        "author": "Anon",
        "isbn": "1234567890",
        "page_count": 120,
        "kind": "book"
    })
    assert r.status_code == 201, r.text
    assert r.json()["isbn"] == "1234567890"

    # Aynı ISBN sahip kitap ekleme testi.
    r = client.post("/books", json={
        "title": "Test Book",
        "author": "Anon",
        "isbn": "1234567890",
        "page_count": 120,
        "kind": "book"
    })
    assert r.status_code == 409

    
    class DummyClient:
        def fetch_by_isbn(self, isbn):
            if isbn == "9780140328721":
                return {"title": "Matilda", "authors": ["Roald Dahl"], "page_count": 240}
            return None

    import external
    monkeypatch.setattr(external, "OpenLibraryClient", lambda *a, **kw: DummyClient())

    # Başarılı ISBN ekleme testi.
    r = client.post("/books/isbn/9780140328721")
    assert r.status_code == 201, r.text
    assert r.json()["title"].lower() == "matilda"

    # Bulunamayan ISBN testi.
    r = client.post("/books/isbn/0000000000")
    assert r.status_code in (400, 404)

    # Kitap silme testi.
    r = client.delete("/books/1234567890")
    assert r.status_code in (200, 204)

    r = client.get("/books")
    assert r.status_code == 200
    titles = [b["title"].lower() for b in r.json()]
    assert "matilda" in titles
