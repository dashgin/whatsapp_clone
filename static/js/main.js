const roomName = JSON.parse(document.getElementById('room-name').textContent);
const user = JSON.parse(document.getElementById('user').textContent);
const messageInput = document.getElementById('chat-message-input');
const messageSendButton = document.getElementById('chat-message-submit');
const messageList = document.querySelector('#conversation');
messageList.scrollTop = messageList.scrollHeight;

const chatSocket = new ReconnectingWebSocket(
    (window.location.protocol === 'https:' ? 'wss' : 'ws') +
    '://' + window.location.host +
    '/ws/chat/' +
    roomName + '/'
);

messageInput.focus();


function emptyChecker(data) {
    if (data !== "" && data !== null && data !== undefined && data !== " ") {
        return true;
    } else {
        return false;
    }
}

function messageBox(data) {
    let message_user = data.user

    let message_user_class = message_user === user ? "sender" : "receiver"

    let image = emptyChecker(data.image) ? `<img src="${data.image}" width="150" height="150">` : ""

    let audio = emptyChecker(data.audio) ? `<audio controls controlslist="nodownload"><source src="${data.audio}" type="audio/mp3"></audio>` : ""

    return (
        `<div class="row message-body">
                    <div class="col-sm-12 message-main-sender">
                        <div class="${message_user_class}">
                            <div class="media">
                              ${image || audio}
                            </div>
                            <div class="message-text">
                                ${data.message}
                            </div>
                            <span class="message-time pull-right">${data.timestamp}</span>
                        </div>
                    </div>
                </div>`
    )
}

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    messageList.innerHTML += messageBox(data);
    messageList.scrollTop = messageList.scrollHeight;

};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

messageInput.onkeyup = function (e) {
    if (e.keyCode === 13) {
        // enter, return
        messageSendButton.click();
    }
};

messageSendButton.onclick = function (e) {
    const message = messageInput.value;
    chatSocket.send(JSON.stringify({
        'message': message,
    }));
    messageInput.value = '';
};

document.getElementById("file").addEventListener("change", handleFileSelect, false);

function handleFileSelect() {
    let file = this.files[0];
    getBase64(file);
}

function getBase64(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
        if (file.type.split('/')[0] === 'image') {
            chatSocket.send(JSON.stringify({
                'image_content': reader.result,
                'message': ''
            }));
        } else if (file.type.split('/')[0] === 'audio') {
            chatSocket.send(JSON.stringify({
                'audio_content': reader.result,
                'message': ''
            }));
        } else {
            alert('Please select an image file')
        }

    };

    reader.onerror = function (error) {
        console.log('Error: ', error);
    };
}

let isRecording = false;
const microphoneBtn = document.getElementById('microphone');

microphoneBtn.onclick = () => {
    if (isRecording) {
        stopRecord()
        microphoneBtn.style.color = ''
        isRecording = false
    } else {
        startRecord()
        microphoneBtn.style.color = 'red'
        isRecording = true
    }
}

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;


function startRecord() {
    navigator.mediaDevices.getUserMedia({audio: true})
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start()
            let audioArray = []

            mediaRecorder.ondataavailable = (e) => {
                audioArray.push(e.data)
            }
            mediaRecorder.onstop = (e) => {
                let audioData = new Blob(audioArray, {'type': 'audio/ogg; codecs=opus'})
                audioArray = []
                console.log(audioData)
                getBase64(audioData)

                stream.getAudioTracks().forEach(function (tracks) {
                    if (tracks.readyState === 'live') {
                        tracks.stop()
                    }
                })
            }

        })
}

function stopRecord() {
    mediaRecorder.stop()
}


