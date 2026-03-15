import cv2
import mediapipe as mp


class PoseEngine:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()


    # Rostro (Puntos 0 al 10)
    # Hombros (Puntos 11 y 12)
    # Caderas (Puntos 23 y 24)
    # Rodillas (Puntos 25 y 26)
    # Tobillos (Puntos 27 y 28)
    def processFrame(self,frame):
        rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        keypoints = []
        index = list(range(0, 13)) + [23, 24, 25, 26, 27, 28]
        
        if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, 
                    results.pose_landmarks, 
                    self.mp_pose.POSE_CONNECTIONS
                )
                
                for i in index:
                    lm = results.pose_landmarks.landmark[i]
                    keypoints.extend([lm.x, lm.y, lm.z, lm.visibility])

        return frame, keypoints
