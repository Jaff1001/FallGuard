import cv2
import mediapipe as mp
import math

class PoseEstimationService:
    """Servicio especializado en la extracción y normalización de telemetría corporal."""
    
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        # Configuración optimizada para inicializar MediaPipe 0.10.x sin problemas
        self.detector = mp.solutions.pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.last_results = None

        # Guarda el valor de la altura de las caderas en el frame anterior
        self.prev_c_y = None

    def reset_state(self):
        """Limpia el estado temporal para empezar a procesar un nuevo vídeo."""
        self.prev_c_y = None

    def _calculate_vertical_velocity(self, current_c_y):
        """Calcula la velocidad vertical del centro de gravedad (eje Y)."""
        if self.prev_c_y is None:
            vel_y = 0.0
        else:
            vel_y = current_c_y - self.prev_c_y
            
        self.prev_c_y = current_c_y
        return vel_y

    def _calculate_spine_angle(self, landmarks, c_x, c_y):
        """Calcula el ángulo de la columna (hombros a caderas) respecto al suelo."""
        mid_shoulder_x = (landmarks[11].x + landmarks[12].x) / 2
        mid_shoulder_y = (landmarks[11].y + landmarks[12].y) / 2
        
        dx_spine = c_x - mid_shoulder_x
        dy_spine = c_y - mid_shoulder_y
        
        return math.degrees(math.atan2(dy_spine, dx_spine))

    def process_telemetry(self, frame):
        """Extrae puntos clave, los normaliza y recopila características dinámicas."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.last_results = self.detector.process(rgb_frame)
        
        if not self.last_results.pose_landmarks:
            return []
        
        landmarks = self.last_results.pose_landmarks.landmark
        BODY_IDX = [0, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

        # Centro de las caderas
        c_x = (landmarks[23].x + landmarks[24].x) / 2
        c_y = (landmarks[23].y + landmarks[24].y) / 2
        
        # 1. Llamada a las funciones de cálculo
        vel_y = self._calculate_vertical_velocity(c_y)
        spine_angle = self._calculate_spine_angle(landmarks, c_x, c_y)

        # 2. Normalización de coordenadas
        dx_scale = landmarks[11].x - landmarks[12].x
        dy_scale = landmarks[11].y - landmarks[12].y
        scale = (dx_scale**2 + dy_scale**2)**0.5 + 1e-6
        
        norm_pts = []
        for idx in BODY_IDX:
            lm = landmarks[idx]    
            norm_x = (lm.x - c_x) / scale
            norm_y = (lm.y - c_y) / scale
            norm_z = lm.z / scale
            norm_pts.extend([norm_x, norm_y, norm_z, lm.visibility])

        norm_pts.extend([vel_y, spine_angle])

        return norm_pts

    def get_face_coords(self):
        """Devuelve las coordenadas correspondientes a la cara del sujeto."""
        if not self.last_results or not self.last_results.pose_landmarks:
            return []
        
        landmarks = self.last_results.pose_landmarks.landmark
        face_landmarks = []

        for i in range(11):
            lm = landmarks[i]
            face_landmarks.extend([lm.x, lm.y, lm.z, lm.visibility])

        return face_landmarks

    def draw_skeleton(self, frame):
        """Dibuja el esqueleto solo con los puntos necesarios."""
        if not self.last_results or not self.last_results.pose_landmarks:
            return frame

        BODY_IDX = [0, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

        # Ocultamos los puntos que no nos interesan
        for i, lm in enumerate(self.last_results.pose_landmarks.landmark):
            if i not in BODY_IDX:
                lm.visibility = 0.0  

        self.mp_drawing.draw_landmarks(
            frame,
            self.last_results.pose_landmarks,
            mp.solutions.pose.POSE_CONNECTIONS
        )
        
        return frame