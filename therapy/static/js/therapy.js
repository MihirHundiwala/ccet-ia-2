const socket = io.connect({ transports: ['websocket'] })
const peer = new Peer(id)
const peers = {}

// Ask for webcam and microphone permissions
navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(stream => {
    // Display your local video in #localVideo element
    localVideo.srcObject = stream;

    peer.on('call', call => {
        peers[call.peer] = call
        call.answer(stream)
        call.on('stream', stream => {
            document.getElementById('remoteVideo').srcObject = stream
            document.getElementById('remoteVideo').hidden = false
            document.getElementById('remotestatus').innerHTML = 'Remote Webcam is On.'
        })
        call.on('close', () => {
            console.log('here')
            document.getElementById('remoteVideo').hidden = true
            document.getElementById('remotestatus').innerHTML = 'Currently,no users connected.'
        })
    })

    socket.on('user-connected', (userid) => {
        document.getElementById('remotestatus').innerHTML = 'User Connected'
        connectToNewUser(userid, stream)
    })
})

socket.on('camera-turned-off', (userid) => {
    document.getElementById('remoteVideo').hidden = true
    document.getElementById('remotestatus').innerHTML = 'Remote Webcam is Off.'
        // console.log('Recieved from server off')

})

socket.on('camera-turned-on', (userid) => {
    document.getElementById('remoteVideo').hidden = false
    document.getElementById('remotestatus').innerHTML = 'Remote Webcam is On.'
        // console.log('Recieved from server on')

})

socket.on('user-disconnected', (userid) => {
    if (peers[userid]) {
        peers[userid].close()
        delete peers[userid]
    }
})


function connectToNewUser(userid, stream) {
    const call = peer.call(userid, stream)

    call.on('stream', remotestream => {
        document.getElementById('remoteVideo').srcObject = remotestream
        document.getElementById('remoteVideo').hidden = false
    })
    call.on('close', () => {
        console.log('here')
        document.getElementById('remoteVideo').hidden = true
        document.getElementById('remotestatus').innerHTML = 'Currently,no users connected.'
    })
    peers[userid] = call
}

peer.on('open', id => {
    socket.emit('join-room', roomid, id)
})

// --------------------------- Toggle-Screen-Audio-Video-tracks -------------------------------

let videoicon = document.getElementById("videoicon")
let micicon = document.getElementById("micicon")
let fullscreenicon = document.getElementById("fullscreenicon")
let video_element = document.getElementsByClassName('video-container')[0]

function videotoggle() {
    if (videoicon.className == "fas fa-video-slash") {
        videoicon.className = "fas fa-video";
        socket.emit('camera-turned-on', roomid, id)
            // localVideo.srcObject.getVideoTracks().forEach(track =>track.play());
            // console.log('sent to server on')
    } else {
        videoicon.className = "fas fa-video-slash";
        socket.emit('camera-turned-off', roomid, id)
            // localVideo.srcObject.getVideoTracks().forEach(track =>track.stop());
            // console.log('sent to server off')
    }
    localVideo.srcObject.getVideoTracks().forEach(track => track.enabled = !track.enabled);
}

function mictoggle() {
    if (micicon.className == "fas fa-microphone-slash") {
        micicon.className = "fas fa-microphone";
    } else {
        micicon.className = "fas fa-microphone-slash";
    }
    // document.getElementById("mic").style.backgroundColor="#F11818";
    localVideo.srcObject.getAudioTracks().forEach(track => track.enabled = !track.enabled);
}

function fullscreentoggle() {
    if (fullscreenicon.className == 'fas fa-expand') {
        fullscreenicon.className = 'fas fa-compress'
        if (video_element.requestFullscreen) {
            video_element.requestFullscreen();
        } else if (video_element.webkitRequestFullscreen) { /* Safari */
            video_element.webkitRequestFullscreen();
        } else if (video_element.msRequestFullscreen) { /* IE11 */
            video_element.msRequestFullscreen();
        }
    } else {
        fullscreenicon.className = 'fas fa-expand'
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) { /* Safari */
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { /* IE11 */
            document.msExitFullscreen();
        }
    }
}

//--------------------------------------------------------------------------------------

function hangup() {
    if (confirm("Leave meeting?")) {
        socket.emit('hang-up', roomid, id)
        window.location = '/'
    }
}

let messages = document.getElementsByClassName('messages')[0];

function sendMessage() {
    text = (document.getElementById('typemsg').value).trim()
    textarea = document.getElementById('typemsg')
    textarea.value = ''
    textarea.style.height = "auto"
    textarea.style.height = (textarea.scrollHeight) + 'px'
    if (text !== "") {
        let now = new Date()
        let time = now.getHours() + ":" + (now.getMinutes()).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false })
        msgdata = { nickname: nickname, time: time, text: text }
        socket.emit('message-to-client', roomid, msgdata)
        let msg = document.createElement('div')
        msg.innerHTML = `<span class="sendername">You</span>
                     <span class="sendtime">${time}</span>
                     <div class="clearfix"></div>
                     <p class="msgbody">${text}</p>`
        msg.className = 'localmsg'
        messages.appendChild(msg)
    }
}

socket.on('message-from-client', (msgdata) => {
    let msg = document.createElement('div')
    msg.innerHTML = `<span class="sendername" style="color: #ab47bccf;">${msgdata['nickname']}</span>
                     <span class="sendtime">${msgdata['time']}</span>
                     <div class="clearfix"></div>
                     <p class="msgbody">${msgdata['text']}</p>`
    msg.className = 'remotemsg'
    messages.append(msg)
})