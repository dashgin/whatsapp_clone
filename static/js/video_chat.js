const firstUser = JSON.parse(document.getElementById('first_user').textContent);
const secondUser = JSON.parse(document.getElementById('second_user').textContent);
const videoMe = document.getElementById('video-me');
const videoPartner = document.getElementById('video-partner');
const microphone = document.getElementById('video-chat-microphone');
const camera = document.getElementById('video-chat-camera');
let isMicEnabled = true;
let isCamEnabled = true;

let side = window.location.search.substr(1).split('=')[1];


const peer = new Peer(
    firstUser,
    {
        debug: 3,
        //     host: 'localhost',
        //     port: 9000,
        //     path: '/myapp/',
        //
    }
)

navigator.mediaDevices.getUserMedia({video: true, audio: true})
    .then(stream => {
        videoMe.srcObject = stream;
        videoMe.play();
        videoMe.muted = true;


        if (side === 'caller') {
            let call = peer.call(secondUser, stream);
            call.on(
                'stream',
                function (remoteStream) {
                    console.log('remoteStream', remoteStream);
                    videoPartner.srcObject = remoteStream;
                    videoPartner.play();
                }
            )
        } else if (side === 'answerer') {
            peer.on(
                'call',
                function (call) {
                    call.answer(stream);
                    call.on(
                        'stream',
                        function (remoteStream) {
                            // console.log('remoteStream', remoteStream);
                            videoPartner.srcObject = remoteStream;
                            videoPartner.play();
                        }
                    )
                }
            )
        }

        camera.addEventListener('click', function () {
            if (isCamEnabled) {
                stream.getVideoTracks()[0].enabled = false;
                isCamEnabled = false;
                camera.classList.add('btn-danger');
            } else {
                stream.getVideoTracks()[0].enabled = true;
                camera.classList.remove('btn-danger');
                isCamEnabled = true;
            }
        });

    });