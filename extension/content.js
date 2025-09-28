function getSelectedImage() {
    try {
        return window.getSelection().getRangeAt(0).cloneContents().querySelector("img");
    } catch (e) {}
    return null;
}

async function getImageDataURL(img) {
    try {
        const canvas = document.createElement("canvas");
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        canvas.getContext("2d").drawImage(img, 0, 0);
        return canvas.toDataURL("image/png");
    } catch {
        try {
            const res = await fetch(img.src);
            const blob = await res.blob();
            return await new Promise((resolve) => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.readAsDataURL(blob);
            });
        } catch {
            return null;
        }
    }
}


document.addEventListener("mouseup", async () => {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    const img = getSelectedImage();

    if (!text && !img) return;

    const imgData = img ? await getImageDataURL(img) : null;
    apiCall(selection, text, imgData);
});


function apiCall(selection, text, img=null) {
    let range, node;
    let nodes = document.body;
    try {
        range = selection.getRangeAt(0);
        node = range.startContainer.parentNode;
    } catch {}

    chrome.runtime.sendMessage(
        { action: "processText", text, image: img },
        async(response) => {
            if (chrome.runtime.lastError) {
                return;
            }
            if (response?.processedText) {
                try {
                    node.title = response.processedText;
                    setTimeout(() => (node.title = ""), 7000);
                    selection.removeAllRanges();
                } catch (e) {}
                try {
                    nodes.title = response.processedText;
                    setTimeout(() => (nodes.title = ""), 7000);
                    selection.removeAllRanges();
                } catch (e) {}

                try {
                    await navigator.clipboard.writeText(response.processedText);
                } catch (e) {}
            }
            if (response?.error) {
                console.error("Error:", response.error);
            }
        }
    );
}
