import os
import io
import base64
import logging
import requests

from google import genai as genai_v2

import google.generativeai as genai

from flask import Flask, request, jsonify, Response
from flask_cors import CORS


logging.basicConfig(level=logging.INFO)

# ---------------- Flask Setup ----------------
app = Flask(__name__)
CORS(app)
app.secret_key = '9202c111s1c6f4ds82df96saf9sd46ds2312fbb9'


# ---------------- Gemini Extension ----------------
class GeminiExtension:
    """
        Encapsulates logic for interacting with Google Gemini API in **two modes**:

        1. **MCQ/Text** (`ask_gemini_mcq`) → For solving objective/short questions.
        2. **Image/OCR** (`ask_gemini_image`) → For extracting readable text from images.

        **Constructor Parameters:**
        * `mode` *(string, required)* → `"mcq"` or `"image"`.
        * `apiKey` *(string, optional)* → Gemini API key (fallback: environment).
        * `Prompt` *(string, optional)* → Override default task-specific prompt.
        * `Questions` *(string, optional)* → Override default few-shot training examples.
        * `text` *(string, optional)* → Question text or MCQ input.
        * `url` *(string, optional)* → Image URL or base64 string.
        * `response` *(bytes, optional)* → Image content in raw bytes.

        **Key Methods:**
        * `gemini_prompt()` → Returns default prompt depending on mode (`mcq` or `image`).
        * `gemini_questions()` → Returns default few-shot Q&A examples.
        * `upload_file_from_url(url, response)` → Converts image input into a streamable object (`BytesIO`).
        * `main()` → Dispatches request to correct handler (`ask_gemini_mcq` or `ask_gemini_image`).
        * `ask_gemini_mcq()` → Uses `google.generativeai` to solve MCQ/text queries.
        * `ask_gemini_image()` → Uses `genai_v2` client for OCR text extraction.

        **Returns:**
        * Always returns a **plain text string** with the AI answer or OCR output.

        **Usage Example (Python call inside backend):**
        ```python
            gemini = GeminiExtension(
                mode="mcq",
                apiKey="your_key_here",
                text="What is the capital of France?",
            )
            result = gemini.main()  # -> "Paris"

            gemini = GeminiExtension(
                mode="image",
                apiKey="your_key_here",
                url="https://stuffs.me/EZbu/"
            )
            result = gemini.main()  # -> "3017f"
        ```
    """
    def __init__(self, mode, apiKey=None, Prompt=None, Questions=None, text=None, url=None, response=None):
        self.apiKey = apiKey or os.getenv("apiKey")
        if not self.apiKey:
            raise ValueError("Missing Gemini API key")

        self.mode = mode or "mcq"
        self.text = text or ""
        self.prompt = Prompt or self.gemini_prompt()
        self.questions = Questions or self.gemini_questions()
        self.bytes_image = self.upload_file_from_url(url, response)

    # Default prompts
    def gemini_prompt(self):
        if self.mode == "image":
            return """**(Extract text from image):**
                You are an OCR assistant. Extract **only** the readable, human-legible text from the provided image.

                * Remove background noise, decorative elements, and artifacts.
                * Preserve actual text, line breaks, and punctuation.
                * Do not include explanations or metadata.
                * If text is illegible, return only `UNREADABLE`."""

        return """**(Q&A with/without options):**
            You are a strict, concise answer bot.

            * If the input question includes options (A, B, C, D or similar), return **only** the single correct option token (e.g., `A`, `B`, `C`, `D`) or `(ans)` if that’s the option format.
            * If the question has no options, return **only** the concise correct answer (one short phrase or number).
            * If the question is an image (with or without options), analyze it and return only the correct option or concise answer.
            * If multiple questions are asked, return answers in order separated by commas (e.g., `B, A, 42`).
            * If the question cannot be answered, return only `INSUFFICIENT_DATA`."""

    def gemini_questions(self):
        return """### **Case 1: With options**
            **Q: 1**
            Which planet is known as the Red Planet?
            A) Earth
            B) Mars
            C) Jupiter
            D) Venus

            **Expected Output:**
            `B`

            ### **Case 2: Without options**
            **Q: 2**
            What is the capital of France?

            **Expected Output:**
            `Paris`

            ### **Case 3: Multiple questions at once**
            **Q: 3**

            1. 2 + 2 = ?
            2. Which gas is most abundant in Earth's atmosphere?
            A) Oxygen
            B) Nitrogen
            C) Carbon Dioxide
            D) Hydrogen

            **Expected Output:**
            `4, B`

            ### **Case 4: Unanswerable**
            **Q: 4**
            What is the password of my Gmail account?

            **Expected Output:**
            `INSUFFICIENT_DATA`"""

    # Upload image (from URL or base64)
    def upload_file_from_url(self, url=None, response=None):
        if not url and not response:
            return None
        try:
            if not response:
                if url.lower().startswith("http"):
                    response = requests.get(url, timeout=10).content
                else:  # Base64
                    _, encoded = url.split(",", 1)
                    response = base64.b64decode(encoded)
            return io.BytesIO(response)

        except Exception as e:
            logging.error(f"Image upload failed: {e}")
            return None

    # Dispatcher
    def main(self, ans=''):
        func_name = f"ask_gemini_{self.mode}"
        func = getattr(self, func_name, None)
        if func and callable(func):
            ans = func().strip()
        logging.info(f"\nAnswer: 👇\n{'--'*50}\n({ans})\n{'--'*50}\n")
        return ans

    # Mode: MCQ / Text
    def ask_gemini_mcq(self):
        try:
            logging.info(f"\nQuestion: 👇\n{'--'*50}\n({self.text})\n{'--'*50}\n")
            genai.configure(api_key=self.apiKey)

            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",
                generation_config = {
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                    "response_mime_type": "text/plain",
                }
            )

            history=[{
                "role": "user",
                "parts": [self.prompt]
            }]

            if self.bytes_image:
                try:
                    history.append({
                        "role": "user",
                        "parts": [genai.upload_file(self.bytes_image, mime_type="image/png")]
                    })
                except:
                    pass

            history.append({
                "role": "user",
                "parts": [self.questions]
            })

            chat_session = model.start_chat(history=history)
            return chat_session.send_message(self.text).text

        except Exception as e:
            logging.error(f"Gemini MCQ error: {e}")
            return ''

    # Mode: Image OCR
    def ask_gemini_image(self):
        text = ""
        try:
            client = genai_v2.Client(api_key=self.apiKey)

            uploaded_file = client.files.upload(
                file=self.bytes_image,
                config={"mime_type": "image/png"}
            )

            contents = [
                genai_v2.types.Content(
                    role="user",
                    parts=[
                        genai_v2.types.Part.from_uri(
                            file_uri=uploaded_file.uri,
                            mime_type=uploaded_file.mime_type,
                        ),
                        genai_v2.types.Part.from_text(
                            text=self.prompt
                        ),
                    ],
                )
            ]

            generate_content_config = genai_v2.types.GenerateContentConfig(
                response_modalities=[
                    "image",
                    "text",
                ],
                response_mime_type="text/plain",
            )
            for chunk in client.models.generate_content_stream(
                model="gemini-2.0-flash-preview-image-generation",
                contents=contents,
                config=generate_content_config,
            ):
                if (
                    chunk.candidates is None
                    or chunk.candidates[0].content is None
                    or chunk.candidates[0].content.parts is None
                ):
                    continue
                if chunk.candidates[0].content.parts[0].inline_data:
                    continue
                else:
                    text += f"{chunk.text}".replace("\n", "").strip()

        except Exception as e:
            logging.error(f"Gemini OCR error: {e}")
            pass

        return text


def get_dynamic(req, param):
    try:
        val = req.get_json(silent=True).get(param)
    except:
        val = req.form.get(param, '') or req.args.get(param, '')

    return val


"""
API endpoint (`/`) that receives user input (MCQ text or image) along with optional configuration parameters,
and delegates the request to the `GeminiExtension` class for processing.

**Workflow:**

1. Extracts request parameters:
   * `mode` *(string)* → `"mcq"` or `"image"`.
   * `apiKey` *(string, optional)* → Overrides environment API key.
   * `Prompt` *(string, optional)* → Custom AI prompt.
   * `Questions` *(string, optional)* → Demo Q&A examples for few-shot prompting.
   * `text` *(string, optional)* → User text input (MCQ, normal question).
   * `image` *(file/base64, optional)* → Uploaded image file or URL/base64 string.

2. Creates a `GeminiExtension` instance with these parameters.

3. Calls the `.main()` dispatcher, which routes to either:
   * `ask_gemini_mcq()` → Handles text/MCQ solving.
   * `ask_gemini_image()` → Handles OCR / image text extraction.

4. Returns a JSON response:
    ```
        {
            "message": "<Gemini response or OCR output>"
        }
    ```

**Error Handling:**
* Returns `{"message": ""}` on failure.
* Logs internal errors without exposing them to client.

**Example Call (MCQ):**

```bash
curl -X POST https://gemini-extensions.vercel.app/ \
    -H "Content-Type: application/json" \
    -d '{
        "mode": "mcq",
        "text": "What is 2+2? A) 3 B) 4 C) 5",
        "apiKey": "your_key_here"
    }'
```

**Example Call (Image):**
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
"""
@app.route('/', methods=['GET', 'POST'])
def ask_question():
    try:
        mode = get_dynamic(request, 'mode')
        apiKey = get_dynamic(request, 'apiKey')
        Prompt = get_dynamic(request, 'Prompt')
        Questions = get_dynamic(request, 'Questions')
        text = get_dynamic(request, 'text')
        try:
            url, response = None, request.files.get('image').read()
        except:
            url, response = get_dynamic(request, 'image') or get_dynamic(request, 'url'), None
        if not mode and not text and not url and not response:
            text = open('README.md', 'r').read()
            response = requests.post(
                "https://api.github.com/markdown",
                headers={"Accept": "application/vnd.github.v3+json"},
                json={"text": text, "mode": "gfm"}
            )
            return Response("""
                <html>
                    <head>
                        <link rel="stylesheet" type="text/css" href="https://krishna.stuffs.me/musicclub/user/folder/assets/css/bootstrap.css">
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-dark.min.css">
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                    </head>
                    <body class="markdown-body p-4">
                        <div class="container">
                            {response.text}
                        </div>
                    </body>
                </html>
            """.replace("{response.text}", response.text))

        output = GeminiExtension(mode, apiKey, Prompt, Questions, text, url, response).main()
        return jsonify({"message": output}), 200

    except Exception as e:
        logging.error(f"Request failed: {e}")
        return jsonify({"message": "", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    """
        gemini = GeminiExtension(
            mode="mcq",
            apiKey="your_key_here",
            url="What is the capital of France?"
        )
        result = gemini.main()  # -> "Paris"
        print(result)

        gemini = GeminiExtension(
            mode="image",
            apiKey="your_key_here",
            url="https://stuffs.me/EZbu/"
        )
        result = gemini.main()  # -> "3017f"
        print(result)
    """
