import cv2
from engines.pose_engine import PoseEngine
from engines.privacy_engine import PrivacyEngine

def main():
    video_capture = cv2.VideoCapture(0)
    pose_estimator = PoseEngine()
    privacy_guardian = PrivacyEngine()

    while True:
        success, raw_frame = video_capture.read()
        if not success: break

        annotated_frame, landmarks = pose_estimator.processFrame(raw_frame)
    
        protected_frame = privacy_guardian.processFrame(annotated_frame, landmarks)

        cv2.imshow('FallGuard Monitoring System', protected_frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()