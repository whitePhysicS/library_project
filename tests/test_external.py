from external import OpenLibraryClient

class DummyResp:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code
    def json(self):
        return self._data
    def raise_for_status(self):        
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

def test_fetch_by_isbn_monkeypatch(monkeypatch):
    client = OpenLibraryClient()

    def fake_get(url, *args, **kwargs):

        timeout = kwargs.get("timeout")
        follow_redirects = kwargs.get("follow_redirects")
        headers = kwargs.get("headers")
        # /isbn/ çağrısı
        if url.endswith("/isbn/9780140328721.json"):
            return DummyResp({
                "title": "Matilda",
                "authors": [{"key": "/authors/OL34184A"}],
                "number_of_pages": 240
            })
        # /authors/ çağrısı
        if url.endswith("/authors/OL34184A.json"):
            return DummyResp({"name": "Roald Dahl"})
        raise AssertionError(f"unexpected url {url}")

    monkeypatch.setattr("httpx.get", fake_get)

    data = client.fetch_by_isbn("9780140328721")
    assert data["title"] == "Matilda"
    assert "Roald Dahl" in data["authors"]
    assert data["page_count"] == 240
