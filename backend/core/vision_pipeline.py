from services.pose_estimator import PoseEstimationService
from utils.anonymizer import AnonymizationHandler
import numpy as np

class VisionPipeline:
    """Se encarga de coordinar la privacidad y la extracción de telemetría."""

    def __init__(self, debug_mode: bool = True):
        self.pose_service = PoseEstimationService()
        self.anonymizer = AnonymizationHandler()
        self.debug_mode = debug_mode

    def reset_state(self):
        """Reinicia el estado interno del estimador de pose para una nueva secuencia de vídeo."""
        self.pose_service.reset_state()

    def execute(self, frame: np.ndarray):
        """Aplica las diferentes capas de procesamiento al fotograma."""
        
        norm_pts = self.pose_service.process_telemetry(frame)
        face_pts = self.pose_service.get_face_coords()
        
        frame = self.pose_service.draw_skeleton(frame)

        if face_pts:
            frame = self.anonymizer.apply_face_blur(frame, face_pts)

        return frame, norm_pts