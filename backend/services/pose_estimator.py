import cv2
import mediapipe as mp

class PoseEstimationService:
    """Servicio especializado en la extracción y normalización de telemetría corporal."""
    
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.detector = mp.solutions.pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.last_results = None

    def process_telemetry(self, frame):
        """Extrae puntos clave brutos y genera una versión normalizada tomando como referencia el centro de las caderas"""
        
  
        rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.last_results = self.detector.process(rgb_frame)
        if not self.last_results.pose_landmarks:
            return [], []
        
        
        landmarks = self.last_results.pose_landmarks.landmark

        # 0: Nariz        |  11-12: Hombros  |  13-14: Codos
        # 15-16: Muñecas  |  23-24: Caderas  |  25-26: Rodillas
        # 27-28: Tobillos
        BODY_IDX = [0, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

        # Normalización de nuevas coordenadas tomando como centro el punto medio de las caderas
        c_x = (landmarks[23].x + landmarks[24].x) / 2
        c_y = (landmarks[23].y + landmarks[24].y) / 2
        
        # Escala: Distancia euclidiana entre hombros usando Pitágoras
        dx = landmarks[11].x - landmarks[12].x
        dy = landmarks[11].y - landmarks[12].y
        scale = (dx**2 + dy**2)**0.5 + 1e-6
        

        norm_pts = []
        for idx in BODY_IDX:
            lm = landmarks[idx]    
            # Puntos Normalizados
            norm_x = (lm.x - c_x) / scale
            norm_y = (lm.y - c_y) / scale
            norm_z = lm.z / scale
            norm_pts.extend([norm_x, norm_y, norm_z, lm.visibility])

        return norm_pts

    
    def get_face_coords(self):
        """Devuelves las cordenadas correspondiantes a la cara del sujeto."""
        if not self.last_results or not self.last_results.pose_landmarks:
            return []
        
        landmarks = self.last_results.pose_landmarks.landmark
        face_landmarks = []

        for i in range(11):
            lm = landmarks[i]
            face_landmarks.extend([lm.x, lm.y, lm.z, lm.visibility])

        return face_landmarks

    
    def draw_skeleton(self, frame):
            """ Dibujar el esqueleto con los puntos necesarios."""
            if not self.last_results or not self.last_results.pose_landmarks:
                return frame

            # 0: Nariz        |  11-12: Hombros  |  13-14: Codos
            # 15-16: Muñecas  |  23-24: Caderas  |  25-26: Rodillas
            # 27-28: Tobillos
            BODY_IDX = [0, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

            # Mediapipe dibuja los puntos con visibilidad, ponemos en 0 aquellos que no esten en la lista
            for i, lm in enumerate(self.last_results.pose_landmarks.landmark):
                if i not in BODY_IDX:
                    lm.visibility = 0.0  

           
            self.mp_drawing.draw_landmarks(
                frame,
                self.last_results.pose_landmarks,
                mp.solutions.pose.POSE_CONNECTIONS
            )
            
            return frame