
# 📘 Book Tracker API 
A small, portfolio-ready project that demonstrates **API fundamentals** (CRUD concepts, REST, HTTP, JSON parsing), using the **Google Books API** to search books and save results to CSV.

> Goal is to develop API skills (design, integration, automation, deployment).

---

## 🚀 What this does
- Searches Google Books by title/keyword.
- Parses the **JSON** response.
- Writes a clean **CSV** with selected fields (title, authors, publisher, publishedDate, categories, pageCount, averageRating, language, infoLink).

---

## 🧰 Tech
- Python 3.10+
- `requests`, `pandas`, `python-dotenv`
- Optional: Postman for manual testing

---

## ▶️ Quickstart

```bash
# 1) (Recommended) create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) (Optional) set a Google Books API key (not required for basic usage)
cp .env.example .env
# then edit .env and set: GOOGLE_BOOKS_API_KEY=your_key

# 4) Run a search
python main.py --q "atomic habits" --max 20 --out data/books_atomic_habits.csv

# 5) Explore the CSV
open data/books_atomic_habits.csv   # macOS (or use your file manager)
```

**Tip:** You can also run without `--out` to print a preview table to the console.

---

## 🧪 Example cURL & Postman

**Raw API (no key required):**
```bash
curl "https://www.googleapis.com/books/v1/volumes?q=atomic+habits&maxResults=5"
```

**Postman steps:**
1. Import the included `postman_collection.json`.
2. Set the `q` query param to your search term.
3. (Optional) Add `key` param if you use an API key.
4. Send and inspect `status`, `headers`, and the JSON body.

---

## 🧩 What to Look For (Learning Punchlist)
- Identify **HTTP method** (GET), endpoint, query params (`q`, `startIndex`, `maxResults`, `key`).
- Read and interpret **JSON** fields (`items[].volumeInfo.*`).
- Handle **pagination** with `startIndex`.
- Implement **basic error handling** (HTTP codes, missing keys).
- Save transformed data to **CSV** for analysis.
- (Stretch) Add **unit tests** and **type hints**.

---

## 🗂 Project Structure

```
book-tracker-api/
├── main.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── postman_collection.json
└── data/
```

---

## 🧱 Extending This Project
- Add flags to filter by language/category.
- Create a `--format json|csv` option.
- Build a small **FastAPI** layer (expose `/search?q=`).
- Schedule a daily run (cron) for a reading list.

---

## ⚖️ License
MIT
