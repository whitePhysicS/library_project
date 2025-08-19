# 📚 Library Project
Python 202 Bootcamp projesi kapsamında geliştirilen Kütüphane Yönetim Sistemidir. Pytest ile kapsayıcı testler içerir.
CLI (terminal arayüzü) - Harici API ile veri zenginleştirme (OpenLibrary) - FastAPI tabanlı REST API aşamalarını içerir.

## Özellikler
- **OOP mimarisi**: Book, EBook, AudioBook, Member, Library.
- **Kalıcı veri**: library.json, members.json (JSON dosyaları).
- **ISBN ile otomatik ekleme**: OpenLibrary API (httpx).
- **CLI**: kitap/üye ekleme, listeleme, silme, ödünç verme–iade.
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
### **POST** `/books/isbn/{isbn}`
OpenLibrary'den başlık/yazar/sayfa sayısı çekerek kitap ekler.
İsteğe bağlı sorgu parametreleri:
- `kind`: `book|ebook|audiobook` (varsayılan `book`)
- `file_format`: ör. `EPUB` (ebook için)
- `duration_in_minutes`: sayı (audiobook için)
- ```bash
  curl -X Post "http://127.0.0.1:8000/books/isbn/9780140328721?kind=book"

### **DELETE** `/books/{isbn}
Kitabı siler. Başarılı durumda **204 No Content** veya **200 OK** dönebilir.

- ```bash
  curl -X DELETE http://127.0.0.1:8000/books/9780132350884

## 💾 Veri Saklama (Önemli)
- `library.json` ve `members.json` **varsayılan olarak** `library.py` **dosyasının bulunduğu dizinde** tutulur







