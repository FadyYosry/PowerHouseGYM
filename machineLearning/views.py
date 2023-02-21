import cv2
import os
from django.http import StreamingHttpResponse

def capture_frames(request):
    cap = cv2.VideoCapture(0)
    # Get the path to the classifier file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    classifier_path = os.path.join(BASE_DIR, 'classifiers/haarcascade_frontalface_default.xml')

# Load the classifier
    detector = cv2.CascadeClassifier(classifier_path)

    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # detect faces in the frame
            faces = detector.detectMultiScale(frame, 1.1, 7)

            # draw a rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # convert the frame to JPEG format
            _, jpeg = cv2.imencode('.jpg', frame)

            # yield the frame as a multipart/x-mixed-replace response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')
