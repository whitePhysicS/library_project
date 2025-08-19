# 📚 Library Project
Python 202 Bootcamp projesi kapsamında geliştirilen Kütüphane Yönetim Sistemidir. Pytest ile kapsayıcı testler içerir.
CLI (terminal arayüzü) - Harici API ile veri zenginleştirme (OpenLibrary) - FastAPI tabanlı REST API aşamalarını içerir.

## Özellikler
- **OOP mimarisi**: Book, EBook, AudioBook, Member, Library.
- **Kalıcı veri**: library.json, members.json (JSON dosyaları).
- **ISBN ile otomatik ekleme**: OpenLibrary API (httpx).
- **CLI (terminal menüsü)**: kitap/üye ekleme, listeleme, silme, ödünç verme–iade.
- **Colorama**: CLI (terminal menüsü) "Colorama" ile desteklendi.
- **REST API (FastAPI)**: Kitap işlemleri (JSON).
- **Testler (pytest)**: Aşama 1–2–3’ün minimum kriterleri kapsanır.

## 🧰 Gereksinimler

- **Python 3.11+**
- **pip**

## Sanal ortam (venv) kullanılması şiddetle tavsiye edilir.
### **Kullanım:**
`python -m venv .venv`
### - Windows
- .venv\Scripts\activate
### - macOS/Linux
- source .venv/bin/activate

## 🛠 Kurulum
- `pip install -r requirements.txt`

# ▶ Nasıl Çalıştırılır

## 1) CLI (Terminal Uygulaması)
#### `python main.py`
Menüden:
- ISBN ile ekle (OpenLibrary),
- Ekle / Sil / Listele / Ara,
- Üye ekle / sil,
- Ödünç ver - iade (ISBN + Member ID),

## 2) API (FastAPI)
#### `uvicorn api:app --reload`
- Swagger UI: http://127.0.0.1:8000/docs
- JSON: http://127.0.0.1:8000/books

# 🧭 API Referansı

### - GET `/books`
Tüm kitapları döndürür.
```bash
curl http://127.0.0.1:8000/books
```
### - **POST** `/books`
İstek gövdesi (JSON):
```json
{
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "isbn": "9780132350884",
  "page_count": 464,
  "kind": "book"          // "book" | "ebook" | "audiobook"
}
```
Ebook örneği:
```json
{
  "title": "eBook",
  "author": "Anon",
  "isbn": "1234567890",
  "page_count": 200,
  "kind": "ebook",
  "file_format": "EPUB"
}
```
AudioBook örneği:
```json
{
  "title": "AudioBook",
  "author": "Anon",
  "isbn": "9999999999",
  "page_count": 0,
  "kind": "audiobook",
  "duration_in_minutes": 75
}
```
### - **POST** `/books/isbn/{isbn}`
OpenLibrary'den başlık/yazar/sayfa sayısı çekerek kitap ekler.
İsteğe bağlı sorgu parametreleri:
- `kind`: `book|ebook|audiobook` (varsayılan `book`)
- `file_format`: ör. `EPUB` (ebook için)
- `duration_in_minutes`: sayı (audiobook için)
- ```bash
  curl -X Post "http://127.0.0.1:8000/books/isbn/9780140328721?kind=book"

### - **DELETE** `/books/{isbn}
Kitabı siler. Başarılı durumda **204 No Content** veya **200 OK** dönebilir.

- ```bash
  curl -X DELETE http://127.0.0.1:8000/books/9780132350884

## 💾 Veri Saklama (Önemli)
- `library.json` ve `members.json` **varsayılan olarak** `library.py` **dosyasının bulunduğu dizinde** tutulur.
- CLI'yi farklı klasörden çalıştırsanız da dosyalar proje klasöründe oluşur.
- Farklı bir konuma yazmak için:
- ```python
  from pathlib import Path
  lib = Library(name="MyLib", base_dir=Path("C:/data"))

# ✅ Testler
## Çalıştırma:
- ```bash
  pytest -q
### Kapsam:
- **Aşama 1 (OOP & CLI temeli)**: `Library`/`Book` temel akışları
- **Aşama 2 (Harici API)**: `OpenLibraryClient` ve `add_book_by_isbn`
  - Başarılı + "bulunamadı" (monkeypatch ile)
- **Aşama 3 (API)**: `GET/POST/DELETE /books`, `POST /books/isbn/{isbn}`
- `tests/conftest.py` import yollarını proje köküne sabitler
- `pytest.ini`:
  ```ini
  [pytest]
  testpaths = tests
  python_files = test_*.py
  addopts = -ra -q
# 📁 Dizin Yapısı
```text
library_project/
  api.py
  external.py
  library.py
  main.py
  library.json
  members.json
  requirements.txt
  pytest.ini
  tests/
    conftest.py
    test_api.py
    test_external.py
    test_external_extra.py
    test_library.py
    test_library_extra.py
```
# 🔮 Geliştirme Fikirleri
- Arama/filtre (`GET /books?title=&author=&kind=`), sayfalama
- CORS (frontend entegrasyonu)
- SQLite/PostgreSQL (JSON yerine DB)
- Kimlik doğrulama (JWT), rol tabanlı yetki
- Dockerize





    








