// Lấy đối tượng video từ webcam và hiển thị lên trình duyệt
function startWebcam() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            var videoElement = document.getElementById('videoElement');
            videoElement.srcObject = stream;

            // Khởi tạo đối tượng Mediapipe
            const pose = new Pose({locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
            }});

            pose.onResults(handleResults);

            videoElement.addEventListener('loadedmetadata', () => {
                pose.send({image: videoElement});
            });
        })
        .catch(function (error) {
            console.log("Error accessing the webcam: ", error);
        });
}

function handleResults(results) {
    var canvas = document.getElementById('outputCanvas');
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Vẽ các vị trí của các bộ phận cơ thể
    // results.poseLandmarks chứa thông tin về các landmarks của cơ thể
}

// Bắt đầu video khi trang đã tải hoàn chỉnh
window.onload = function () {
    startWebcam();
};
