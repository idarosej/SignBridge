function updateGesture() {

    fetch("/gesture")
        .then(response => response.text())
        .then(data => {

            document.getElementById("gestureText").innerHTML = data;

        })
        .catch(error => {

            console.log(error);

        });

}

async function updateHistory() {

    const response = await fetch("/history");

    const data = await response.json();

    const list = document.getElementById("historyList");

    list.innerHTML = "";

    data.history.forEach(item => {

        const li = document.createElement("li");

        li.textContent = item;

        list.appendChild(li);

    });

}

async function updateConfidence(){

    const response = await fetch("/confidence");

    const data = await response.json();

    document.getElementById("confidenceText").innerText =
        data.confidence + "%";

    document.getElementById("confidenceBar").style.width =
        data.confidence + "%";

}

setInterval(updateConfidence,500);


setInterval(updateHistory, 1000);

// Update immediately
updateGesture();

// Update every 300ms
setInterval(updateGesture, 300);