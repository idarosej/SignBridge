// ===============================
// UPDATE CURRENT GESTURE
// ===============================

async function updateGesture() {

    try {

        const response = await fetch("/gesture");

        if (!response.ok) {
            throw new Error("Gesture request failed");
        }

        const data = await response.text();

        const gestureText =
            document.getElementById("gestureText");

        if (gestureText) {
            gestureText.innerText = data;
        }

    } catch (error) {

        console.log("Gesture error:", error);

    }
}


// ===============================
// UPDATE CONFIDENCE
// ===============================

async function updateConfidence() {

    try {

        const response = await fetch("/confidence");

        if (!response.ok) {
            throw new Error("Confidence request failed");
        }

        const data = await response.json();

        const confidence =
            Number(data.confidence) || 0;

        const confidenceText =
            document.getElementById("confidenceText");

        const confidenceBar =
            document.getElementById("confidenceBar");


        if (confidenceText) {

            confidenceText.innerText =
                confidence.toFixed(1) + "%";

        }


        if (confidenceBar) {

            confidenceBar.style.width =
                Math.min(confidence, 100) + "%";

        }

    } catch (error) {

        console.log("Confidence error:", error);

    }
}


// ===============================
// UPDATE GESTURE HISTORY
// ===============================

async function updateHistory() {

    try {

        const response = await fetch("/history");

        if (!response.ok) {
            throw new Error("History request failed");
        }

        const data = await response.json();

        const list =
            document.getElementById("historyList");

        if (!list) {
            return;
        }

        list.innerHTML = "";


        data.history.forEach(function(item) {

            const li =
                document.createElement("li");

            li.textContent = item;

            list.appendChild(li);

        });

    } catch (error) {

        console.log("History error:", error);

    }
}


// ===============================
// START UPDATES
// ===============================

// Run immediately
updateGesture();
updateConfidence();
updateHistory();


// Current gesture
setInterval(updateGesture, 300);


// Confidence
setInterval(updateConfidence, 500);


// History
setInterval(updateHistory, 1000);
// ===============================
// UPDATE SESSION STATISTICS
// ===============================

async function updateStats() {

    try {

        const response = await fetch("/stats");

        if (!response.ok) {
            throw new Error("Statistics request failed");
        }

        const data = await response.json();

        const total =
            document.getElementById("totalGestures");

        const mostDetected =
            document.getElementById("mostDetected");

        const bestConfidence =
            document.getElementById("bestConfidence");

        if (total) {
            total.innerText = data.total;
        }

        if (mostDetected) {
            mostDetected.innerText =
                data.most_detected;
        }

        if (bestConfidence) {
            bestConfidence.innerText =
                data.highest_confidence + "%";
        }

    } catch (error) {

        console.log("Statistics error:", error);

    }
}
updateStats();

setInterval(updateStats, 1000);
// ===============================
// SESSION STATISTICS
// ===============================

async function updateStats() {

    try {

        const response = await fetch("/stats");

        if (!response.ok) {
            throw new Error("Failed to load statistics");
        }

        const data = await response.json();

        document.getElementById("totalGestures").innerText =
            data.total;

        document.getElementById("mostDetected").innerText =
            data.most_detected;

        document.getElementById("bestConfidence").innerText =
            data.highest_confidence + "%";

    } catch (error) {

        console.log("Statistics error:", error);

    }
}


// Update statistics immediately
updateStats();

// Update statistics every second
setInterval(updateStats, 1000);

// ===============================
// RESET SESSION
// ===============================

async function resetSession() {

    try {

        const response = await fetch("/reset-session", {
            method: "POST"
        });

        const data = await response.json();

        if (data.success) {

            document.getElementById("totalGestures").innerText = "0";

            document.getElementById("mostDetected").innerText = "None";

            document.getElementById("bestConfidence").innerText = "0%";

            document.getElementById("historyList").innerHTML = "";

            document.getElementById("gestureText").innerText =
                "No Hand Detected";

            document.getElementById("confidenceText").innerText =
                "0%";

            document.getElementById("confidenceBar").style.width =
                "0%";

            console.log("Session reset successfully");

        }

    } catch (error) {

        console.log("Reset error:", error);

    }
}