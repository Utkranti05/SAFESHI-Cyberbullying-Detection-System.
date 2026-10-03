const messageInput = document.getElementById("messageInput");
const characterCount = document.getElementById("characterCount");
const detectButton = document.getElementById("detectButton");

const resultCard = document.getElementById("resultCard");
const resultCategory = document.getElementById("resultCategory");
const resultConfidence = document.getElementById("resultConfidence");
const resultIcon = document.getElementById("resultIcon");


// Character counter
messageInput.addEventListener("input", function () {
    characterCount.textContent = `${this.value.length}/1000`;
});


// Detect button
detectButton.addEventListener("click", async function () {

    const text = messageInput.value.trim();

    if (!text) {
        alert("Please enter a message first.");
        return;
    }

    detectButton.disabled = true;
    detectButton.textContent = "Analyzing...";
    

    try {

        const response = await fetch(" https://safeshi-cyberbullying-detection-system.onrender.com", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        // Show result
        resultCard.classList.remove("hidden");

        resultCategory.textContent = data.category;
        resultConfidence.textContent =
            `Confidence: ${data.confidence}%`;

        // Change icon
        if (data.category === "Non-Bullying") {
            resultIcon.textContent = "✓";
        } else {
            resultIcon.textContent = "!";
        }
                // ---- SEVERITY (added) ----
        const level = getSeverity(data.category, data.confidence);
        resultCard.dataset.severity = level;

        if (level === "uncertain") {
            resultConfidence.textContent += " (low confidence, this may be a false alarm)";
        }

        resultCard.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });

    } catch (error) {

        alert(
            error instanceof TypeError
                ? "Could not connect to SAFESHI server.\n\nMake sure Flask is running."
                : error.message
        );

        console.error(error);
        // ---- GIBBERISH CHECK (added) ----
    if (looksLikeGibberish(text)) {
        resultCard.classList.remove("hidden");
        resultCategory.textContent = "Not enough to analyze";
        resultConfidence.textContent = "Please type a real sentence so SAFESHI can check it.";
        resultIcon.textContent = "?";
        resultCard.dataset.severity = "uncertain";   // uses the yellow style you already have
        return;                                      // stops here, no call to Flask
    }

    } finally {

        detectButton.disabled = false;
        detectButton.textContent = "🔍  Analyze Message";
    }
});

// Decides the color level from the category name + confidence (added)
function getSeverity(category, confidence) {
    const c = category.toLowerCase();

    if (c === "non-bullying") return "safe";   // green
    if (confidence < 60) return "uncertain";   // yellow
    if (c.includes("threat") || c.includes("hate") || c.includes("misogyn")) {
        return "high";                         // red
    }
    return "medium";                           // orange (insult, harassment, etc.)
}

// Highlight the nav link of the section currently on screen (added)
const navLinks = document.querySelectorAll(".navbar nav a");
const navObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            navLinks.forEach((link) => {
                link.classList.toggle(
                    "active",
                    link.getAttribute("href") === "#" + entry.target.id
                );
            });
        }
    });
}, { rootMargin: "-45% 0px -50% 0px" });

document.querySelectorAll("section[id]").forEach((s) => navObserver.observe(s));
