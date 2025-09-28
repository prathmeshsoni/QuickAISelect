<p id="top" align="center"></p>

# Gemini Extension 🚀

This is a simple **Chrome Extension** + **Flask API** that allows you to:
1. Solve **MCQs** instantly.
2. Extract **text from images** (like CAPTCHA).

<br>

## Demo Video 🎥

![MCQ-Mode](https://github.com/user-attachments/assets/72bff0d5-3f79-4945-853d-f033a40f2082)

![Image-OCR-Mode](https://github.com/user-attachments/assets/be199c38-1ce7-4ed4-a38b-395b52da31a2)

<br>

## ✨ Features
- One-time setup (settings saved in cookies).
- Toggle between **MCQ Mode** and **Image OCR Mode**.
- Powered by **Gemini AI**.
- Works directly while selecting text on any webpage.

<br>

## 🛠️ How to Use

### 1. Setup Backend

1. Clone Repository

   ```bash
   git clone https://github.com/PrathmeshSoni/QuickAISelect.git && cd QuickAISelect
   ```

2. Install Python 3.9+

3. Setup Virtual Environment

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

4. Install Dependencies

   ```bash
   pip install -r backend/requirements.txt
   ```

5. Run the server:

   ```bash
   python backend/app.py
   ```

   Backend runs at: `http://127.0.0.1:5000`

### 2. Setup Chrome Extension

https://github.com/user-attachments/assets/84733e02-401c-4dd6-9250-9e8d8db8c36f

1. Open **Chrome** → Go to `chrome://extensions/`
2. Enable **Developer Mode** (top right).
3. Click **Load unpacked** → Select the `extension/` folder.
4. Open the extension popup → Enter:

   * Your **Gemini API Key**
   * Backend endpoint → `http://127.0.0.1:5000`
5. Click **Save Settings** (saved in cookies).

### 3. Run the Extension

1. Select any **text** on a webpage.
2. Wait **4–6 seconds** → The text will automatically unselect (API processed).
3. Hover over the **starting point** of your selection.
4. 🎉 Answer appears as a **tooltip**.

<br>

## Full Demo Video 🎥

https://github.com/user-attachments/assets/39a24e66-b692-4017-91b6-9ca12b9c3744

https://github.com/user-attachments/assets/7029fa91-7458-47b3-84f2-46d945bb5f94

<br>

## Demo Flow

1. Load extension → Enter settings once.
2. Run `python app.py`.
3. Select text → Auto-unselect → Hover → See AI Answer.

<br>

## ✅ Example Use Cases

* Solve MCQs while practising online.
* Extract text from CAPTCHA-like images.
* Quickly get AI-powered hints or answers from selected text.


<br />
<br />

The repository is a starting point for most of my professional projects; for this, I'm using it as a part of my portfolio. Feel free to use it wherever you want. I'll be happy if you provide any feedback, code improvements or suggestions.

<br />

## Connect with me at

<p align='center'>
  <a href="https://www.linkedin.com/in/PrathmeshSoni/" target="_blank">
    <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
</p>

<p align='center'>
  📫 How to reach me: <a href='mailto:connect.prathmeshsoni@gmail.com'>connect.prathmeshsoni@gmail.com</a>
</p>


## All Set :)

<p style="float:left;" align="left">
  <a href="#top">Back To Top</a>
</p>

<p style="text-align:right;" align="right">
  <a href="https://github.com/PrathmeshSoni/QuickAISelect" target="_blank">Back To Repository</a>
</p>

---

**<a href="https://soniprathmesh.com?ref=footer-github" target="_blank">QuickAISelect</a>** - Provided by **<a href="https://soniprathmesh.com?ref=footer-github" target="_blank">Prathmesh Soni</a>**
