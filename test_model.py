from ultralytics import YOLO

model = YOLO(
    "runs/detect/runs/agroia_soil-3/weights/best.pt"
)

results = model.predict(
    source="dataset/test/images",
    conf=0.10,
    save=True
)

for result in results:
    print("\nImagen:", result.path)

    if result.boxes is None or len(result.boxes) == 0:
        print("Sin detecciones")
        continue

    for box in result.boxes:
        clase_id = int(box.cls[0])
        confianza = float(box.conf[0])
        clase = result.names[clase_id]

        print(
            f"Clase: {clase} | "
            f"Confianza: {confianza:.2f}"
        )

