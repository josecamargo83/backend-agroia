# **API Agro**
from ultralytics import YOLO

# Modelo base de YOLO
model = YOLO("yolo11n.pt")

# Entrenamiento del modelo
results = model.train(
    data="dataset/data.yaml",
    epochs=25,
    imgsz=640,
    project="runs",
    name="agroia_soil_2clases",
)

print("Entrenamiento finalizado.")
print("El modelo entrenado se encuentra en la carpeta runs.")
