from django.urls import path
from .views import capture_frames,face_detection, classifyPose ,stream_camera, pose_classifier

urlpatterns = [
    path('stream_camera/', stream_camera, name='stream_camera'),
    path('face_detection/', face_detection, name='face_detection'),
    path('classify_pose/', classifyPose, name='classify_pose'),
    path('capture_frames/', capture_frames, name='capture_frames'),
    path('pose_classifier/', pose_classifier, name='pose_classifier'),
]
