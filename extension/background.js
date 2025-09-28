const DEFAULT_URL = "https://gemini-extensions.vercel.app";

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    chrome.storage.local.get(
        ["status", "mode", "url", "apiKey", "customPromptmcq", "customPromptimage", "demoQuestionsmcq", "demoQuestionsimage"],
        (data) => {
            if (data.status == "off") {
                sendResponse({ error: "Extension is turned off." });
                return;
            }
            const mode = data.mode;
            const url = data.url;
            const apiKey = data.apiKey;
            let Prompt = mode === "mcq" ? data.customPromptmcq : data.customPromptimage;
            let Questions = mode === "mcq" ? data.demoQuestionsmcq : data.demoQuestionsimage;

            const payload = {
                mode: mode,
                apiKey: apiKey,
                Prompt: Prompt,
                Questions: Questions,
                text: request.text,
                ...(request.image && { image: request.image })
            };

            fetch(url || DEFAULT_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            })
            .then(res => {
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return res.json();
            })
            .then(data => sendResponse({ processedText: data?.message ?? "" }))
            .catch(err => sendResponse({ error: "Failed to process request." }));
        }
    );

    return true;
});
