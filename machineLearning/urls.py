from django.urls import path
from .views import capture_frames,face_detection, classifyPose ,classify_pose_real_time , stream_camera

urlpatterns = [
    path('', stream_camera, name='stream_camera'),
    path('face_detection/', face_detection, name='face_detection'),
    path('classify_pose/', classifyPose, name='classify_pose'),
    path('classify_pose_real_time/', classify_pose_real_time, name='classify_pose_real_time'),
    path('capture_frames/', capture_frames, name='capture_frames'),
]
