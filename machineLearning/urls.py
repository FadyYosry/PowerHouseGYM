from django.urls import path
from .views import capture_frames,face_detection, classifyPose ,classify_pose_real_time , stream_camera, pose_classifier, classify_pose_real_time2

urlpatterns = [
    path('', stream_camera, name='stream_camera'),
    path('face_detection/', face_detection, name='face_detection'),
    path('classify_pose/', classifyPose, name='classify_pose'),
    path('classify_pose_real_time/', classify_pose_real_time, name='classify_pose_real_time'),
    path('classify_pose_real_time2/', classify_pose_real_time2, name='classify_pose_real_time2'),
    path('capture_frames/', capture_frames, name='capture_frames'),
    path('pose_classifier/', pose_classifier, name='pose_classifier'),
]
