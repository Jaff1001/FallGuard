from services.pose_estimator import PoseEstimationService
from utils.anonymizer import AnonymizationHandler
import numpy as np

class VisionPipeline:
    """Se encarga de coordinar la privacidad y la telemetría."""

    def __init__(self, debug_mode: bool = True):
        self.pose_service = PoseEstimationService()
        self.anonymizer = AnonymizationHandler()
        self.debug_mode = debug_mode

    def execute(self, frame: np.ndarray):
        """Se encarga de añadir las diferentes capas al frame."""
        norm_pts = self.pose_service.process_telemetry(frame)
        face_pts = self.pose_service.get_face_coords()
        frame = self.pose_service.draw_skeleton(frame)

        frame = self.anonymizer.apply_face_blur(frame, face_pts)

        return frame, norm_pts