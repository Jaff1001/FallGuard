import cv2

class PrivacyEngine:
    # ======================================================================
    # DIAGRAMA DE COORDENADAS PARA EL RECORTE (ROI)
    # ======================================================================
    # (0,0) Origen (Top-Left) ------------------------> Eje X (Ancho / w)
    #   |
    #   |       (x1, y1)  <-- Punto Mínimo (Esquina Superior Izquierda)
    #   |          *---------------------------*
    #   |          |      MARGEN (PADDING)     |
    #   |          |    *-----------------* |
    #   |  Eje Y   |    |                 |    |
    #   | (Alto/h) |    |     ROSTRO      |    |
    #   |          |    |   (Puntos 0-10) |    |
    #   |          |    *-----------------* |
    #   |          |                           |
    #   v          *---------------------------* (x2, y2)
    #                                            Punto Máximo (Bottom-Right)
    #
    # Lógica de OpenCV: frame[y1:y2, x1:x2]
    # ======================================================================
   def processFrame(self, frame, keypoints):
        if not keypoints:
            return frame
        
        h, w, _ = frame.shape
        xs = []
        ys = []
        for i in range(0, 11):
            xs.append(int(keypoints[i*4] * w))
            ys.append(int(keypoints[i*4 + 1] * h))

        padding = 40
        x1, y1 = max(0, min(xs) - padding), max(0, min(ys) - padding)
        x2, y2 = min(w, max(xs) + padding), min(h, max(ys) + padding)

        face_roi = frame[y1:y2, x1:x2]
        if face_roi.size > 0:
            face_roi = cv2.GaussianBlur(face_roi, (99, 99), 30)
            frame[y1:y2, x1:x2] = face_roi

        return frame