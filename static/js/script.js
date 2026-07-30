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

// Update immediately
updateGesture();

// Update every 300ms
setInterval(updateGesture, 300);