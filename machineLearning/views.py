import cv2
from django.http import StreamingHttpResponse

def capture_frames(request):
    cap = cv2.VideoCapture(0)

    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # process the frame here

            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')
