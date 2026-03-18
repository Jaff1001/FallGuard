import cv2
import os
import numpy as np
from core.vision_pipeline import VisionPipeline

def run_live_monitor():
    """Ejecuta el proceso sobre la webcam"""
    video_capture = cv2.VideoCapture(0)
    pipeline = VisionPipeline(debug_mode=True)

    while True:
        success, raw_frame = video_capture.read()
        if not success: 
            print("Error: No se pudo acceder a la cámara.")
            break

        processed_frame, telemetry_data = pipeline.execute(raw_frame)
    
        cv2.imshow('FallGuard Enterprise Monitoring System', processed_frame)

        if cv2.waitKey(1) & 0xFF == 27: 
            break

    video_capture.release()
    cv2.destroyAllWindows()

def run_static_test_image():
    """Ejecuta el proceso sobre una imagen fijada"""
    pipeline = VisionPipeline(debug_mode=True)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.abspath(os.path.join(script_dir, "..", "data", "tests", "images", "pose.jpg"))
    image = cv2.imread(image_path)
    
    processed_image, telemetry_data = pipeline.execute(image)

    cv2.namedWindow("FallGuard Analysis", cv2.WINDOW_NORMAL)

    cv2.resizeWindow("FallGuard Analysis", 800, 600)

    cv2.imshow("FallGuard Analysis", processed_image)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_live_monitor()