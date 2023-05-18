from io import BytesIO
import json
import cv2
import os
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
import mediapipe as mp
import math
import numpy as np
from django.views.decorators.csrf import csrf_exempt
import base64


def face_detection(request):
    if request.method == 'POST':
        # Get the video frame data from POST data
        video_frame = request.POST.get('videoFrame')

        # Perform face detection on the video frame
        # Replace this with your face detection logic
        # You can use a face detection library such as OpenCV or dlib
        # Example using OpenCV:
        # frame = cv2.imdecode(np.fromstring(video_frame, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        # faces = detect_faces(frame)
        # results = process_faces(faces)

        # Replace the above example with your face detection logic
        # and format the results in a dictionary or list as needed
        results = {'status': 'success', 'message': 'Faces detected and processed'}

        # Send the results back to the client as JSON
        return JsonResponse(results)

    else:
        # Return an error response if the request method is not POST
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

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

# Combine the two views into a single view
def face_detection_with_camera(request):
    if request.method == 'POST':
        # Get the video frame data from POST data
        video_frame = request.POST.get('videoFrame')

        # Perform face detection on the video frame
        # Replace this with your face detection logic
        # You can use a face detection library such as OpenCV or dlib
        # Example using OpenCV:
        # frame = cv2.imdecode(np.fromstring(video_frame, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        # faces = detect_faces(frame)
        # results = process_faces(faces)

        # Replace the above example with your face detection logic
        # and format the results in a dictionary or list as needed
        results = {'status': 'success', 'message': 'Faces detected and processed'}

        # Send the results back to the client as JSON
        return JsonResponse(results)

    else:
        # Return the streaming video frames
        cap = cv2.VideoCapture(0)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# For testing 
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils 

def detectPose(image, pose, display=False):
    output_image = image.copy()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    height, width, _ = image.shape
    landmarks = []
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS)
        for landmark in results.pose_landmarks.landmark:
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                  (landmark.z * width)))
    return output_image, landmarks

def calculateAngle(landmark1, landmark2, landmark3):
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360
    return angle


def classifyPose(landmarks, output_image, display=False):
    label = 'Unknown Pose'
    color = (0, 0, 255)
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
    if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:
        if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:
            if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:
                if left_knee_angle > 90 and left_knee_angle < 120 or right_knee_angle > 90 and right_knee_angle < 120:
                    label = 'Warrior II Pose' 
            if left_knee_angle > 160 and left_knee_angle < 195 and right_knee_angle > 160 and right_knee_angle < 195:
                label = 'T Pose'
    if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:
        if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45:
            label = 'Tree Pose'
    if label != 'Unknown Pose':
        color = (0, 255, 0)  
    cv2.putText(output_image, label, (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    return output_image, label

@csrf_exempt
async def classify_pose_real_time(request):
    if request.method == 'GET': 
        # Start capturing video from the camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return HttpResponseBadRequest('Failed to open video capture from this device.')

        # Initialize pose detection and classification models
        pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

        # Set up the response headers
        response = StreamingHttpResponse(await generate_frames(cap, pose_video), content_type='multipart/x-mixed-replace; boundary=frame')

        # Release the video capture device
        cap.release()

        # Return the response
        return response
    else:
        return HttpResponseNotAllowed(['GET'])

async def generate_frames(cap, pose_video):
    while True:
        # Read a new frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Detect the pose and classify it
        output_image, landmarks = detectPose(frame, pose_video)
        if landmarks:
            output_image, label = classifyPose(landmarks, output_image)
        else:
            label = 'No Pose Detected'

        # Encode the output image as a JPEG and yield it as a response
        _, jpeg = cv2.imencode('.jpg', output_image)
        yield b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: ' + str(len(jpeg)).encode() + b'\r\n\r\n' + jpeg.tobytes() + b'\r\n'

    # Release the video capture device
    cap.release()


def stream_camera(request):
    def stream_frames():
        pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
        camera_video = cv2.VideoCapture(0)
        camera_video.set(3, 1280)
        camera_video.set(4, 960)

        while camera_video.isOpened():
            ok, frame = camera_video.read()
            if not ok:
                continue
            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))
            frame, landmarks = detectPose(frame, pose_video, display=False)
            if landmarks:
                frame, _ = classifyPose(landmarks, frame, display=False)

            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        camera_video.release()

    return StreamingHttpResponse(stream_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

@csrf_exempt
def pose_classifier(request):
    if request.method == "POST":
        image = request.FILES['image']
        pose = mp.solutions.pose.Pose()
        output_image, landmarks = detectPose(image, pose)
        label = classifyPose(landmarks, output_image)

        # Create a new file object from the image data.
        file_object = BytesIO()
        file_object.write(image.read())

        # Return the image data as a JSON response.
        return HttpResponse(json.dumps({
            "image": file_object.getvalue(),
            "label": label
        }))

    else:
        return HttpResponse("Invalid request method.")

@csrf_exempt
async def classify_pose_real_time2(request):
    if request.method == 'GET':
        # Start capturing video from the camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return HttpResponseBadRequest('Failed to open video capture from this device.')

        # Initialize pose detection and classification models
        pose_video = mp.solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

        # Set up the response headers
        response = StreamingHttpResponse(generate_frames2(cap, pose_video), content_type='multipart/x-mixed-replace; boundary=frame')

        # Release the video capture device
        cap.release()

        # Return the response
        return response
    else:
        return HttpResponseNotAllowed(['GET'])


async def generate_frames2(cap, pose_video):
    while True:
        # Read a new frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Detect the pose and classify it
        output_image, landmarks = await detectPose(frame, pose_video)
        if landmarks:
            output_image, label = await classifyPose(landmarks, output_image)
        else:
            label = 'No Pose Detected'

        # Encode the output image as a JPEG and yield it as a response
        _, jpeg = cv2.imencode('.jpg', output_image)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n'
               b'Content-Length: ' + str(len(jpeg)).encode() + b'\r\n'
               b'\r\n' + jpeg.tobytes() + b'\r\n')

    # Release the video capture device
    cap.release()