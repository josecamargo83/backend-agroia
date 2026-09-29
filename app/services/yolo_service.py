from pathlib import Path

from ultralytics import YOLO


# ============================================================
# RUTA BASE DEL PROYECTO
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


# ============================================================
# MODELO YOLO ENTRENADO
# ============================================================

MODEL_PATH = BASE_DIR / "models" / "best.pt"


# ============================================================
# CARGAR MODELO
# ============================================================

model = YOLO(str(MODEL_PATH))


# ============================================================
# ANALIZAR IMAGEN
# ============================================================

def analizar_imagen(imagen_path: str):

    resultados = model.predict(
        source=imagen_path,
        conf=0.25,
        save=False
    )

    detecciones = []

    for resultado in resultados:

        if resultado.boxes is None:
            continue

        for box in resultado.boxes:

            clase_id = int(box.cls[0])
            confianza = float(box.conf[0])

            coordenadas = box.xyxy[0].tolist()

            x_min = int(coordenadas[0])
            y_min = int(coordenadas[1])
            x_max = int(coordenadas[2])
            y_max = int(coordenadas[3])

            nombre_clase = resultado.names[clase_id]

            detecciones.append({
                "clase": nombre_clase,
                "confianza": confianza,
                "x_min": x_min,
                "y_min": y_min,
                "x_max": x_max,
                "y_max": y_max
            })

    return detecciones


# ============================================================
# ANALIZAR FRAME DE CÁMARA
# ============================================================

def analizar_frame(frame):

    resultados = model.predict(
        source=frame,
        conf=0.25,
        save=False,
        verbose=False
    )

    detecciones = []

    for resultado in resultados:

        if resultado.boxes is None:
            continue

        for box in resultado.boxes:

            clase_id = int(box.cls[0])

            confianza = float(box.conf[0])

            coordenadas = box.xyxy[0].tolist()

            x_min = int(coordenadas[0])
            y_min = int(coordenadas[1])
            x_max = int(coordenadas[2])
            y_max = int(coordenadas[3])

            nombre_clase = resultado.names[clase_id]

            detecciones.append({
                "clase": nombre_clase,
                "confianza": confianza,
                "x_min": x_min,
                "y_min": y_min,
                "x_max": x_max,
                "y_max": y_max
            })

    return detecciones