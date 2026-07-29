async function openCamera() {

    const video = document.getElementById("video");

    const section = document.getElementById("camera-section");

    section.style.display = "block";

    try {

        const stream = await navigator.mediaDevices.getUserMedia({
            video: true
        });

        video.srcObject = stream;

    }

    catch(err){

        alert("Unable to access camera.");

    }

}