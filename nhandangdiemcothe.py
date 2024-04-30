from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

app = Flask(__name__)

# Khởi tạo đối tượng Mediapipe với các giá trị min_detection_confidence và min_tracking_confidence tùy chỉnh
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Hàm sinh các khung hình từ webcam
def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Không thể kết nối với camera.")
        return

    # Sử dụng Mediapipe với các giá trị min_detection_confidence và min_tracking_confidence tùy chỉnh
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Không thể đọc khung hình từ camera.")
                break

            # Xử lý khung hình để nhận diện và vẽ các landmarks
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Chuyển đổi hình ảnh thành dữ liệu dạng jpeg và trả về
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
