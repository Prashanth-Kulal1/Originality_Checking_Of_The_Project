const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const fileLabel = document.getElementById("fileLabel");

/* DRAG EVENTS */
["dragenter", "dragover", "dragleave", "drop"].forEach(event => {
    dropZone.addEventListener(event, e => {
        e.preventDefault();
        e.stopPropagation();
    });
});

["dragenter", "dragover"].forEach(event => {
    dropZone.addEventListener(event, () => {
        dropZone.style.borderColor = "#22c55e";
    });
});

["dragleave", "drop"].forEach(event => {
    dropZone.addEventListener(event, () => {
        dropZone.style.borderColor = "#38bdf8";
    });
});

/* DROP FILE */
dropZone.addEventListener("drop", e => {
    const files = e.dataTransfer.files;

    if (files.length > 0) {
        fileInput.files = files;
        fileLabel.innerText = "📄 " + files[0].name;
    }
});

/* CLICK SELECT */
fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        fileLabel.innerText = "📄 " + fileInput.files[0].name;
    }
});

/* ANALYZE FUNCTION */
async function analyze() {
    const file = fileInput.files[0];

    if (!file) {
        alert("Upload a file first");
        return;
    }

    const resultsDiv = document.getElementById("results");
    resultsDiv.style.display = "block";
    resultsDiv.innerHTML = "<h2>⏳ Processing...</h2>";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        resultsDiv.innerHTML = `
            <h2>📊 Analysis Results</h2>

            <div class="summary">
                <div class="card">
                    <h3>AI Detection</h3>
                    <p>${data.ai_detection}</p>
                </div>

                <div class="card">
                    <h3>Plagiarism Score</h3>
                    <p>${data.plagiarism_score}%</p>
                </div>
            </div>

            <h3>🚨 Plagiarized Content</h3>
            <div id="highlight"></div>

            <br>
            <button onclick="download()">📥 Download Report</button>
        `;

        const highlightDiv = document.getElementById("highlight");

        if (!data.highlighted || data.highlighted.length === 0) {
            highlightDiv.innerHTML = "<p>✅ No plagiarism detected</p>";
        } else {
            data.highlighted.forEach(sentence => {
                const div = document.createElement("div");
                div.className = "highlight-text";
                div.innerText = sentence;
                highlightDiv.appendChild(div);
            });
        }

    } catch (err) {
        resultsDiv.innerHTML = "<p style='color:red;'>Error occurred</p>";
    }
}

function download() {
    window.location.href = "/download";
}