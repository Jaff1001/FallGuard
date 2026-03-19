import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

def load_dataset(csv_path, window_size=30):
    """
    Carga el CSV y lo transforma en ventanas temporales 3D para la LSTM.
    """
    df = pd.read_csv(csv_path)
    
    # Seleccionamos las columnas de características (las 54 que procesa el pipeline)
    # Saltamos 'video_id' y 'frame_number'. La última es 'label'.
    feature_cols = df.columns[2:-1]
    
    # 1. Normalización: Es vital para que la LSTM aprenda rápido
    scaler = StandardScaler()
    df[feature_cols] = scaler.fit_transform(df[feature_cols])
    
    # Guardamos el scaler para usarlo luego en la App de tiempo real
    joblib.dump(scaler, 'scaler.pkl')
    print("✓ Scaler guardado como 'scaler.pkl'")

    X = []
    y = []

    # 2. Creación de ventanas por video_id para no mezclar sujetos
    for vid, group in df.groupby('video_id'):
        features = group[feature_cols].values
        label = group['label'].iloc[0]
        
        # Si el video es más corto que la ventana, lo saltamos o podrías hacer padding
        if len(features) < window_size:
            continue
            
        # Deslizamos la ventana (overlap de 5 frames para generar más datos)
        for i in range(0, len(features) - window_size, 5):
            window = features[i : i + window_size]
            X.append(window)
            y.append(label)
            
    return np.array(X), np.array(y)

def build_lstm_model(input_shape):
    """
    Define la arquitectura de la red neuronal.
    """
    model = tf.keras.Sequential([
        # Capa de entrada: recibe [30 frames, 54 datos]
        tf.keras.layers.Input(shape=input_shape),
        
        # Primera capa LSTM: 64 unidades con memoria
        # return_sequences=True es necesario para conectar con otra capa LSTM
        tf.keras.layers.LSTM(64, return_sequences=True),
        tf.keras.layers.Dropout(0.2), # Evita el sobreajuste (overfitting)
        
        # Segunda capa LSTM: resume la secuencia en un vector
        tf.keras.layers.LSTM(32),
        tf.keras.layers.Dropout(0.2),
        
        # Capas densas para la clasificación final
        tf.keras.layers.Dense(16, activation='relu'),
        
        # Capa de salida: Sigmoid nos da un valor entre 0 y 1 (probabilidad)
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train():
    # Parámetros
    CSV_FILE = "fall_dataset.csv"
    WINDOW_SIZE = 30 # Aproximadamente 1 segundo de video
    
    # --- PASO 1: Preparar Datos ---
    print("Preparando secuencias temporales...")
    X, y = load_dataset(CSV_FILE, window_size=WINDOW_SIZE)
    
    # Dividir en 80% entrenamiento y 20% validación
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Forma de X_train: {X_train.shape}") # Debería ser (N, 30, 54)
    
    # --- PASO 2: Construir Modelo ---
    model = build_lstm_model(input_shape=(WINDOW_SIZE, 54))
    model.summary() # Muestra la estructura de la red
    
    # --- PASO 3: Entrenar ---
    print("\nIniciando entrenamiento...")
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        'best_model.h5', save_best_only=True, monitor='val_loss'
    )
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=32,
        callbacks=[checkpoint]
    )
    
    # --- PASO 4: Guardar ---
    model.save('fall_detection_model.h5')
    print("\n✓ Modelo final guardado como 'fall_detection_model.h5'")

if __name__ == "__main__":
    train()