# Gemini Extension API (Developer Docs)

This repo contains:
1. A **Flask backend** to connect with Gemini API.
2. A **Chrome Extension** that uses the backend for MCQ solving and Image/OCR text extraction.

This document is meant for developers who want to **extend or customize** the functionality.

---

## 🔧 Features
- Solve **MCQs** with options.
- Extract **text from images** (CAPTCHA-like).
- Store settings in **cookies** for persistence.
- Chrome extension integrated with backend API.
- Optional **custom prompts** and **training examples**.

---

## 📂 Project Structure
```

project/
│── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│── extension/
│   ├── logo/
│   │   ├── icon16.png
│   │   ├── icon32.png
│   │   ├── icon48.png
│   │   ├── icon128.png
│   ├── scripts/
│   │   ├── bootstrap.js
│   │   ├── popup.js
│   ├── styles/
│   │   ├── popup.css
│   ├── background.js
│   ├── content.js
│   ├── manifest.json
│   ├── popup.html
│── README.dev.md           # Developer docs
│── README.md               # User docs
│── LICENSE

```

---

## 📡 API Documentation

### Endpoint
```

POST /

````

### Parameters
| Name        | Type        | Required | Description |
|-------------|-------------|----------|-------------|
| `mode`      | string      | ✅       | `"mcq"` or `"image"` |
| `apiKey`    | string      | ❌       | Gemini API key (overrides env) |
| `Prompt`    | string      | ❌       | Custom AI prompt |
| `Questions` | string      | ❌       | Few-shot training examples |
| `text`      | string      | ❌       | Question text (for MCQ mode) |
| `image`     | file/base64 | ❌       | Image file or base64 string (for OCR mode) |

---

### 📝 Example Request (MCQ Mode)
```bash
curl -X POST https://gemini-extensions.vercel.app/ \
    -H "Content-Type: application/json" \
    -d '{
        "mode": "mcq",
        "text": "Which planet is known as the Red Planet? A) Earth B) Mars C) Venus D) Jupiter",
        "apiKey": "your_key_here"
    }'
````

**Response:**

```json
{
  "message": "B"
}
```

---

### 📝 Example Request (Image OCR Mode)

```bash
curl -X POST https://gemini-extensions.vercel.app/ \
    -F "mode=image" \
    -F "image=@captcha.png" \
    -F "apiKey=your_key_here"
```

```bash
curl -X POST https://gemini-extensions.vercel.app/ \
    -H "Content-Type: application/json" \
    -d '{
        "mode": "image",
        "url": "https://stuffs.me/EZbu/",
        "apiKey": "your_key_here"
    }'
```

**Response:**

```json
{
  "message": "3017f"
}
```

---

## 🛠️ Core Class: `GeminiExtension`

Encapsulates Gemini API logic for both MCQ and OCR modes.

### Example (Python usage)

```python
from app import GeminiExtension

# MCQ
gemini = GeminiExtension(
    mode="mcq",
    apiKey="your_key_here",
    text="What is the capital of France?"
)
print(gemini.main())  # -> "Paris"

# OCR
gemini = GeminiExtension(
    mode="image",
    apiKey="your_key_here",
    url="https://stuffs.me/EZbu/"
)
print(gemini.main())  # -> "3017f"
```

---

## ⚠️ Error Handling

* Returns `{ "message": "" }` if no valid output.
* Returns `{ "error": "details" }` if server-side error.
* Logs inputs and outputs.
