let userIndex = NaN;
let questionIndex = NaN;

document.addEventListener("DOMContentLoaded", function () {
    let microfono = document.getElementById("microfono");
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    let active = true;
    getIndex();

    microfono.addEventListener("click", () => {
        if (!isRecording && active) {
            document.getElementById("texto-microfono").textContent = "Detener grabación";
            document.getElementById("texto-microfono").style.color = "white";
            microfono.style.backgroundColor = "red";
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then((stream) => {
                    mediaRecorder = new MediaRecorder(stream);

                    mediaRecorder.ondataavailable = (event) => {
                        if (event.data.size > 0) {
                            audioChunks.push(event.data);
                            console.log(event.data);
                        }
                    };

                    mediaRecorder.onstop = async () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

                        console.log("aquí se enviará la grabación");
                        let response = await sendAudio(audioChunks[0]);
                        document.getElementById("texto-microfono").textContent = "Utilizar micrófono";
                        active = true;

                        document.getElementById("id_text").value = response;
                        audioChunks = [];
                    };

                    mediaRecorder.start();
                    isRecording = true;
                })
                .catch((error) => {
                    console.error('Error al acceder al micrófono:', error);
                });
        } else if (active) {
            document.getElementById("texto-microfono").textContent = "Transcribiendo";
            document.getElementById("texto-microfono").style.color = "rgba(112, 112, 112, 1)";
            microfono.style.backgroundColor = "white";
            if (mediaRecorder) {
                active = false;
                mediaRecorder.stop();
                isRecording = false;
            }
        }

    });


});

function getIndex() {
    let url = window.location.href;
    let partsUrl = url.split("/");
    let indexPreguntas = partsUrl.indexOf("preguntas");

    if (indexPreguntas !== -1 && indexPreguntas < partsUrl.length - 1) {
        userIndex = partsUrl[indexPreguntas + 1];
        questionIndex = partsUrl[indexPreguntas + 2]
        console.log("Número después de 'preguntas':", userIndex);
    } else {
        console.log("No se encontró un número después de 'preguntas'.");
    }
}

function sendAudio(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio');

    return fetch(`http://localhost:8000/audio/${userIndex}/${questionIndex}/`, {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            return data.message;
        })
        .catch(error => {
            console.error("Hubo un error:", error);
            alert("Error en el Servidor o no hay conexión al mismo \n Tipo de Error: \n " + error);
            return "No hay conexión con el servidor";
        });
}