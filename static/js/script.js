// ===============================
// UPDATE GESTURE
// ===============================

async function updateGesture() {

    try {

        const response = await fetch("/gesture");
        const data = await response.text();

        const gestureText =
            document.getElementById("gestureText");

        const sessionStatus =
            document.getElementById("sessionStatus");

        const statusDot =
            document.getElementById("statusDot");


        if (gestureText) {
            gestureText.innerText = data;
        }


        if (data.trim() === "No Hand Detected") {

            if (sessionStatus) {
                sessionStatus.innerText = "Waiting for Hand";
            }

            if (statusDot) {
                statusDot.style.backgroundColor = "#A67B5B";
            }

        } else {

            if (sessionStatus) {
                sessionStatus.innerText = "Hand Detected";
            }

            if (statusDot) {
                statusDot.style.backgroundColor = "#4CAF50";
            }

        }

    } catch (error) {

        console.log("Gesture error:", error);

    }
}



// ===============================
// UPDATE HISTORY
// ===============================

async function updateHistory() {

    try {

        const response = await fetch("/history");

        if (!response.ok) {
            return;
        }

        const data = await response.json();

        const list =
            document.getElementById("historyList");

        if (!list) {
            return;
        }

        list.innerHTML = "";

        if (data.history && data.history.length > 0) {

           data.history.forEach(item => {

                const li = document.createElement("li");

                li.textContent = item;

                list.appendChild(li);

          });

        } else {

             const li = document.createElement("li");

             li.textContent = "No gestures detected yet";

             li.style.color = "#999";

             list.appendChild(li);

      }

    } catch (error) {

        console.log("History error:", error);

    }
}



// ===============================
// UPDATE CONFIDENCE
// ===============================

async function updateConfidence() {

    try {

        const response = await fetch("/confidence");

        if (!response.ok) {
            return;
        }

        const data = await response.json();

        const confidenceText =
            document.getElementById("confidenceText");

        const confidenceBar =
            document.getElementById("confidenceBar");


        if (confidenceText) {

            confidenceText.innerText =
                Number(data.confidence).toFixed(1) + "%";

        }


        if (confidenceBar) {

            confidenceBar.style.width =
                data.confidence + "%";

        }

    } catch (error) {

        console.log("Confidence error:", error);

    }
}



// ===============================
// UPDATE SESSION STATISTICS
// ===============================

async function updateStats() {

    try {

        const response = await fetch("/stats");

        if (!response.ok) {
            return;
        }

        const data = await response.json();

        console.log("Session Stats:", data);


        const totalGestures =
            document.getElementById("totalGestures");

        const mostDetected =
            document.getElementById("mostDetected");

        const bestConfidence =
            document.getElementById("bestConfidence");
        const sessionDuration =
             document.getElementById("sessionDuration");
        const differentGestures =
    document.getElementById("differentGestures");

        if (totalGestures) {

            totalGestures.innerText =
                data.total;

        }


        if (mostDetected) {

            mostDetected.innerText =
                data.most_detected;

        }


        if (bestConfidence) {

            bestConfidence.innerText =
                Number(data.highest_confidence).toFixed(1) + "%";

        }
        if (sessionDuration) {

            const totalSeconds =
                Number(data.session_duration);

            const minutes =
                Math.floor(totalSeconds / 60);

            const seconds =
                totalSeconds % 60;

            sessionDuration.innerText =
                String(minutes).padStart(2, "0") +
                ":" +
                String(seconds).padStart(2, "0");
}
        if (differentGestures) {

            differentGestures.innerText =
                        data.different_gestures;

        }

    } catch (error) {

        console.log("Stats error:", error);

    }
}



// ===============================
// START DASHBOARD
// ===============================

updateGesture();
updateHistory();
updateConfidence();
updateStats();


// ===============================
// AUTO UPDATE
// ===============================

setInterval(updateGesture, 300);

setInterval(updateHistory, 1000);

setInterval(updateConfidence, 500);

setInterval(updateStats, 1000);

// ===============================
// RESET SESSION
// ===============================

async function resetSession() {

    try {

        const response = await fetch("/reset-session", {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error("Reset request failed");
        }

        const data = await response.json();

        console.log(data);

        if (data.success) {

            // Immediately refresh everything
            await updateGesture();
            await updateHistory();
            await updateConfidence();
            await updateStats();

        }

    } catch (error) {

        console.log("Reset error:", error);

    }
}