import cv2
import numpy as np

class AnonymizationHandler:
    """Se encarga de censurar caras para mantener la privacidad."""

    def apply_face_blur(self, frame, keypoints):
        """Detecta la región del rostro y aplica un desenfoque Gaussiano."""
        if len(keypoints) == 0:
            return frame
        
        h, w, _ = frame.shape
        xs, ys = [], []
        
        for i in range(11):
            if (i * 4 + 1) < len(keypoints):
                xs.append(int(keypoints[i*4] * w))
                ys.append(int(keypoints[i*4 + 1] * h))


        padding = 40
        x1, y1 = max(0, min(xs) - padding), max(0, min(ys) - padding)
        x2, y2 = min(w, max(xs) + padding), min(h, max(ys) + padding)

        roi = frame[y1:y2, x1:x2]
        frame[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (99, 99), 30)

        return frame