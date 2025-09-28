// --- Utility: Cookie Handling ---
function getCookie(name) {
    return new Promise((resolve) => {
        chrome.storage.local.get([name], (data) => {
            resolve(data[name] || "");
        });
    });
}


// --- Default Values ---
const DEFAULT_PROMPT = {
    mcq: `(Q&A with/without options): You are a strict, concise answer bot.

If the input question includes options (A, B, C, D or similar), return only the single correct option token (e.g., A, B, C, D) or (ans) if that’s the option format.

If the question has no options, return only the concise correct answer (one short phrase or number).

If the question is an image (with or without options), analyze it and return only the correct option or concise answer.

If multiple questions are asked, return answers in order separated by commas (e.g., B, A, 42).

If the question cannot be answered, return only INSUFFICIENT_DATA.`,

    image: `(Extract text from image): You are an OCR assistant. Extract only the readable, human-legible text from the provided image.

Remove background noise, decorative elements, and artifacts.
Preserve actual text, line breaks, and punctuation.
Do not include explanations or metadata.
If text is illegible, return only UNREADABLE.`
};

const DEFAULT_QUESTION = {
    mcq: `Case 1: With options

Q: 1) Which planet is known as the Red Planet? A) Earth B) Mars C) Jupiter D) Venus
Expected Output: B

Case 2: Without options

Q: 2) What is the capital of France?
Expected Output: Paris

Case 3: Multiple questions at once

Q: 3)
2 + 2 = ?
Which gas is most abundant in Earth's atmosphere? A) Oxygen B) Nitrogen C) Carbon Dioxide D) Hydrogen
Expected Output: 4, B

Case 4: Unanswerable

Q: 4) What is the password of my Gmail account?
Expected Output: INSUFFICIENT_DATA`,

    image: ``
};


// --- Load Settings from Cookie ---
window.onload = async () => {
    let status = await getCookie("status") || "on";
    document.getElementById("ExtensionToggle").checked = status === "on";
    let url = await getCookie("url");
    document.getElementById("url").value = url;
    const mode = await getCookie("mode") || "mcq";
    document.querySelector("input[id='modeToggle']").checked = mode === "image";
    let apiKey = await getCookie("apiKey") || "";
    document.getElementById("apiKey").value = apiKey;

    // Load mode-specific values
    loadModeValues(mode);

    // Attach toggle change listener
    document.querySelector("input[id='modeToggle']").addEventListener("change", handleModeChange);

    const customPrompt = document.getElementById("customPrompt").value.trim();
    const demoQuestions = document.getElementById("demoQuestions").value.trim();
    chrome.storage.local.set({
        status: status,
        url: url,
        mode: mode,
        apiKey: apiKey,
        ["customPrompt" + mode]: customPrompt,
        ["demoQuestions" + mode]: demoQuestions
    }, () => {
        console.log("✅ Init Saved settings to chrome.storage.local");
    });
};

// --- Load mode-specific values ---
async function loadModeValues(mode) {
    document.getElementById("customPrompt").value = await getCookie("customPrompt" + mode);
    document.getElementById("customPrompt").placeholder = DEFAULT_PROMPT[mode];
    document.getElementById("demoQuestions").value = await getCookie("demoQuestions" + mode);
    document.getElementById("demoQuestions").placeholder = DEFAULT_QUESTION[mode];
    document.getElementById("demoQuestionsDiv").classList.toggle("hidden", mode !== "mcq");
}

// --- Handle Toggle Change ---
function handleModeChange() {
    const mode = document.querySelector("input[id='modeToggle']").checked ? "image" : "mcq";
    loadModeValues(mode);
}

// --- Save Button ---
document.getElementById("saveBtn").addEventListener("click", () => {
    const status = document.getElementById("ExtensionToggle").checked ? "on" : "off";
    const url = document.getElementById("url").value.trim();
    const mode = document.querySelector("input[id='modeToggle']").checked ? "image" : "mcq";
    const apiKey = document.getElementById("apiKey").value.trim();
    const customPrompt = document.getElementById("customPrompt").value.trim();
    const demoQuestions = document.getElementById("demoQuestions").value.trim();

    chrome.storage.local.set({
        status: status,
        url: url,
        mode: mode,
        apiKey: apiKey,
        ["customPrompt" + mode]: customPrompt,
        ["demoQuestions" + mode]: demoQuestions
    }, () => {
        console.log("✅ Saved settings to chrome.storage.local");
    });

    alert("✅ Settings saved successfully for " + mode.toUpperCase() + " mode!");
});
