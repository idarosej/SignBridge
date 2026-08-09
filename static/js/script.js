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