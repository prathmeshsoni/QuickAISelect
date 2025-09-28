<p id="top" align="center"></p>

# Gemini Extension 🚀

A lightweight **Chrome Extension** + **Flask API** that lets you instantly:

1. Solve **MCQs** on any webpage.
2. Extract **text from images** (like CAPTCHA or screenshots).

<br>

## 🎥 Demo Preview

**MCQ Mode**

![MCQ-Mode](https://github.com/user-attachments/assets/72bff0d5-3f79-4945-853d-f033a40f2082)

**Image OCR Mode**

![Image-OCR-Mode](https://github.com/user-attachments/assets/be199c38-1ce7-4ed4-a38b-395b52da31a2)


<br>

## ✨ Features

* 🧠 Dual modes → **MCQ Solver** & **Image Text Extractor**
* 💾 One-time setup (settings saved in cookies)
* 🔁 Toggle mode easily in pop-up
* ⚙️ Powered by **Gemini AI**
* 🧷 **Auto answer copy** → Answer is automatically copied to the clipboard for quick use
* 🖱️ Works directly on any webpage by selecting text


<br>

## ⚙️ Setup Guide

### 1️⃣ Backend Setup

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

### 2️⃣ Chrome Extension Setup

https://github.com/user-attachments/assets/84733e02-401c-4dd6-9250-9e8d8db8c36f

1. Open **Chrome** → Go to `chrome://extensions/`
2. Enable **Developer Mode** (top right).
3. Click **Load unpacked** → Select the `extension/` folder.
4. Open the extension popup → Enter:

   * Your **Gemini API Key**
   * Backend endpoint → `http://127.0.0.1:5000`
5. Click **Save Settings** (saved in cookies).

### 3️⃣ How to Use

1. Select **any text** or **text with image** on a webpage
2. Wait **4–6 seconds** → Text auto-unselects (means API processed)
3. Hover over the **starting point** of your selection
4. 💬 AI Answer appears as a **tooltip**
5. 📋 **Answer is auto-copied** to your clipboard instantly

<br>

## 🎬 Full Demo Videos

https://github.com/user-attachments/assets/39a24e66-b692-4017-91b6-9ca12b9c3744

https://github.com/user-attachments/assets/8636a4ad-f82f-4daf-958a-b747b9be5093

<br>

## 🧩 Demo Flow

1. Load extension and save your settings
2. Run backend using `python app.py`
3. Select text → Wait → Hover → Get answer → Copied to clipboard automatically

<br>

## 💡 Example Use Cases

- ✅ Solve MCQs instantly while studying online
- ✅ Extract text from CAPTCHA-like or blurry images
- ✅ Quickly get AI-powered hints, explanations, or answers
- ✅ Save time — no need to copy, paste, or type manually

<br />

## 💡 Other Use Cases

* **Instant Definitions:** Highlight any unfamiliar term or acronym on a webpage — GeminiSelect gives a quick, clean definition.
* **Concept Linking:** Select a topic (e.g., “Neural Networks”), and Gemini provides related key ideas or subtopics to explore further.
* **Email Drafting Help:** Select text from an email or message thread to generate a polite or professional reply.
* **Productivity Aid:** Highlight action items or meeting notes to generate a to-do list automatically.
* **Learning Companion:** Select complex academic content to get simplified, beginner-friendly explanations.
* **Fact Checking:** Highlight a statement or claim and verify its accuracy with AI-backed context.
* **Creative Support:** Select part of a story or article and ask Gemini to continue or reimagine it.
* **SEO / Copywriting:** Select marketing text to get improved, keyword-optimised alternatives.
* **Mathematical Queries:** Highlight an equation or problem statement — get the step-by-step solution.
* **Web Research Helper:** Select a topic or sentence and get a concise overview, key stats, or insights.
* **Code Refactoring:** Highlight inefficient or unclear code — Gemini suggests an optimised rewrite.
* **Error Explanation:** Highlight any error log or browser console message to instantly understand the cause.
* **Data Insight:** Highlight data in a table or report — get summaries, insights, or quick interpretations.

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
