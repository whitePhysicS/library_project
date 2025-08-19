import httpx

class OpenLibraryClient:
    BASE = "https://openlibrary.org"

    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    def _get(self, path: str):
        url = f"{self.BASE}{path}"
        r = httpx.get(
            url,
            timeout=self.timeout,
            follow_redirects=True,          
            headers={"User-Agent": "LibraryApp/1.0"}  
        )
        r.raise_for_status()
        return r.json()
    
    def fetch_by_isbn(self, isbn: str) -> dict | None:
        try:
            data = self._get(f"/isbn/{isbn}.json")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

        except httpx.RequestError:
            return None
        

        title = data.get("title")

        author_names: list[str] = []

        for a in data.get("authors",[]):
            key = a.get("key")
            if not key:
                continue
            try:
                ajson = self._get(f"{key}.json")
                name = ajson.get("name")
                if name:
                    author_names.append(name)
            except Exception:
                continue

        page_count = data.get("number_of_pages")

        return {
            "title": title,
            "authors": author_names or ["Unknown"],
            "page_count": page_count,
        }