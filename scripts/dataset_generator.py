import os
import cv2
import pandas as pd
import sys

# Aseguramos que Python encuentre la carpeta 'backend'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.services.pose_estimator import PoseEstimationService

def process_video(video_path, video_id, label, pose_service):
    """
    Abre un vídeo, extrae la telemetría frame a frame y la estructura para el CSV.
    """
    video_data = []
    cap = cv2.VideoCapture(video_path)

    # Reiniciar la memoria de velocidad vertical para cada vídeo nuevo
    pose_service.reset_state() 
    
    frame_number = 0
    last_valid_pts = None
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Obtenemos los 54 valores (52 coords + vel_y + spine_angle)
        norm_pts = pose_service.process_telemetry(frame)
        
        # Si no hay detección, usamos el último frame conocido (Forward Fill)
        if not norm_pts and last_valid_pts is not None:
            norm_pts = last_valid_pts
        
        if norm_pts:
            # Estructura: [ID, Frame] + [54 valores] + [Label] = 57 columnas
            row = [video_id, frame_number] + norm_pts + [label]
            video_data.append(row)
            last_valid_pts = norm_pts
            
        frame_number += 1
        
    cap.release()
    return video_data

def createDataset():
    """
    Navega por la estructura de carpetas de sujetos y categorías para generar el CSV.
    """
    BASE_PATH = "data/Video"
    OUTPUT_CSV = "data/Csv/fall_dataset.csv"
    
    if not os.path.exists(BASE_PATH):
        print(f"Error: No se encuentra la carpeta {BASE_PATH}")
        return

    # Definición de nombres de columnas
    body_parts = ['nose', 'l_shoulder', 'r_shoulder', 'l_elbow', 'r_elbow', 
                  'l_wrist', 'r_wrist', 'l_hip', 'r_hip', 'l_knee', 'r_knee', 
                  'l_ankle', 'r_ankle']
    
    # 1. Identificadores (2 columnas)
    csv_columns = ['video_id', 'frame_number']

    # 2. Puntos MediaPipe (52 columnas: 13 puntos * 4 valores cada uno)
    for part in body_parts:
        csv_columns.extend([f'{part}_x', f'{part}_y', f'{part}_z', f'{part}_v'])
    
    # 3. Características calculadas (2 columnas)
    csv_columns.extend(['vel_y', 'spine_angle'])

    # 4. Etiqueta final (1 columna)
    csv_columns.append('label')
    # TOTAL COLUMNAS: 2 + 52 + 2 + 1 = 57

    all_data = []
    pose_service = PoseEstimationService()

    # Navegación por Sujetos
    subject_folders = [f for f in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, f))]

    for subject_name in subject_folders:
        subject_path = os.path.join(BASE_PATH, subject_name)
        category_folders = [f for f in os.listdir(subject_path) if os.path.isdir(os.path.join(subject_path, f))]
        
        for category_name in category_folders:
            category_path = os.path.join(subject_path, category_name) 
            
            # Etiqueta automática basada en el nombre de la carpeta
            label = 1 if category_name.lower() == "fall" else 0
            
            # Filtrar solo archivos mp4
            mp4_files = [f for f in os.listdir(category_path) if f.endswith('.mp4')]

            for video_file in mp4_files:
                video_path = os.path.join(category_path, video_file)
                video_id = f"{subject_name}_{category_name}_{video_file}"
                
                print(f"Procesando: {video_id} | Clase: {label}")
                
                # Procesar el vídeo y extender la lista maestra
                video_rows = process_video(video_path, video_id, label, pose_service)
                all_data.extend(video_rows)

    # Guardar el resultado
    if all_data:
        print("\nGenerando archivo CSV...")
        df = pd.DataFrame(all_data, columns=csv_columns)
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"¡Éxito! Dataset guardado en: {OUTPUT_CSV}")
        print(f"Total de registros: {len(df)} filas y {len(csv_columns)} columnas.")
    else:
        print("No se encontraron datos para procesar.")

if __name__ == "__main__":
    createDataset()