
# Text Similarity REST API

A RESTful API and Streamlit frontend to compare similarity between two texts or text files using **TF-IDF** and **Semantic (BERT)** methods.

---

## Features

- Compare similarity between manually entered texts or uploaded files
- Supports TF-IDF and Semantic similarity using Sentence Transformers
- Lightweight FastAPI backend
- Interactive Streamlit frontend for easy usage
- Simple test script to validate API endpoints

---

## Installation

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd <your-project-folder>
````

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the API

Start the FastAPI server with:

```bash
uvicorn app.main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## API Endpoints

* `GET /`
  Returns a welcome message.

* `POST /compare-texts/`
  Compare similarity between two texts submitted as form data.
  **Form fields:**

  * `text1`: first text (string)
  * `text2`: second text (string)
  * `method`: similarity method, `"tfidf"` or `"semantic"` (optional, default `"tfidf"`)

* `POST /compare-files/`
  Compare similarity between two uploaded text files.
  **Form fields:**

  * `file1`: first text file (txt)
  * `file2`: second text file (txt)
  * `method`: similarity method, `"tfidf"` or `"semantic"` (optional, default `"tfidf"`)

---

## Streamlit Frontend

To run the interactive frontend:

```bash
streamlit run streamlit_app.py
```

Features:

* Input texts manually or upload files
* Select similarity method
* View similarity score and method used
* Keeps history of recent comparisons

---

## Testing the API

Use `test_api.py` to quickly test both text and file comparison endpoints.
Place files to compare in the same directory as the script.

Run:

```bash
python test_api.py
```

---

## Project Structure

```
app/
├── __init__.py
├── main.py               # FastAPI backend routes
├── similarity_engine.py  # TF-IDF and Semantic similarity logic
├── utils.py              # Text cleaning utility
streamlit_app.py          # Streamlit frontend
test_api.py               # API test script
requirements.txt          # Dependencies
```

---

## Notes

* Semantic similarity uses the `all-MiniLM-L6-v2` Sentence Transformer model, loaded once at startup for performance.
* Input texts are cleaned (lowercased, punctuation removed) before similarity computation.
* API returns similarity score (0 to 1) and percentage similarity.
* Proper error handling is implemented for invalid methods or inputs.

---

## License

[MIT License](LICENSE)

```

---

Feel free to replace `<your-repo-url>` and `<your-project-folder>` with your actual repo URL and folder name.

If you want, I can also help generate the **LICENSE** file or a shorter **Contributing** section for the README. Just say the word!
```