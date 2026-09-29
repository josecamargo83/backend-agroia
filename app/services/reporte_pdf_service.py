from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from datetime import datetime
from pathlib import Path


def generar_reporte_pdf(
    ruta_salida,
    archivo_imagen,
    detecciones,
    telemetria
):

    ruta_salida = Path(ruta_salida)

    doc = SimpleDocTemplate(
        str(ruta_salida),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    estilos = getSampleStyleSheet()

    elementos = []

    # ============================================================
    # TITULO
    # ============================================================

    elementos.append(
        Paragraph(
            "AGROIA - REPORTE DE ANÁLISIS DE SUELO",
            estilos["Title"]
        )
    )

    elementos.append(
        Spacer(1, 15)
    )

    elementos.append(
        Paragraph(
            f"Fecha del reporte: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Spacer(1, 20)
    )

    # ============================================================
    # CRITERIO 1 - YOLO
    # ============================================================

    elementos.append(
        Paragraph(
            "1. Detección del suelo mediante YOLO",
            estilos["Heading2"]
        )
    )

    elementos.append(
        Spacer(1, 8)
    )

    if detecciones:

        datos_detecciones = [
            [
                "Clase",
                "Confianza",
                "Bounding Box"
            ]
        ]

        for deteccion in detecciones:

            bbox = deteccion.get(
                "bbox",
                {}
            )

            datos_detecciones.append(
                [
                    deteccion.get(
                        "clase",
                        "-"
                    ),
                    f"{deteccion.get('confianza', 0) * 100:.2f}%",
                    (
                        f"({bbox.get('x1', '-')}, "
                        f"{bbox.get('y1', '-')}) - "
                        f"({bbox.get('x2', '-')}, "
                        f"{bbox.get('y2', '-')})"
                    )
                ]
            )

        tabla = Table(
            datos_detecciones,
            colWidths=[
                1.5 * inch,
                1.2 * inch,
                2.5 * inch
            ]
        )

        tabla.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.grey
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.black
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (1, -1),
                    "CENTER"
                )
            ])
        )

        elementos.append(tabla)

    else:

        elementos.append(
            Paragraph(
                "No se detectaron objetos en la imagen.",
                estilos["Normal"]
            )
        )

    elementos.append(
        Spacer(1, 20)
    )

    # ============================================================
    # CRITERIO 2 - CONDICIONES AMBIENTALES
    # ============================================================

    elementos.append(
        Paragraph(
            "2. Condiciones ambientales",
            estilos["Heading2"]
        )
    )

    elementos.append(
        Spacer(1, 8)
    )

    temperatura = telemetria.get(
        "temp_aire",
        "-"
    )

    humedad_aire = telemetria.get(
        "humedad_aire",
        "-"
    )

    tabla_ambiental = Table([
        ["Parámetro", "Valor"],
        ["Temperatura del aire", f"{temperatura} °C"],
        ["Humedad del aire", f"{humedad_aire} %"]
    ], colWidths=[3 * inch, 2.5 * inch])

    tabla_ambiental.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            )
        ])
    )

    elementos.append(
        tabla_ambiental
    )

    elementos.append(
        Spacer(1, 20)
    )

    # ============================================================
    # CRITERIO 3 - PARÁMETROS DEL SUELO
    # ============================================================

    elementos.append(
        Paragraph(
            "3. Parámetros del suelo",
            estilos["Heading2"]
        )
    )

    elementos.append(
        Spacer(1, 8)
    )

    humedad_suelo = telemetria.get(
        "humedad_suelo",
        "-"
    )

    ph = telemetria.get(
        "ph",
        "-"
    )

    tds = telemetria.get(
        "tds",
        "-"
    )

    tabla_suelo = Table([
        ["Parámetro", "Valor"],
        ["Humedad del suelo", f"{humedad_suelo} %"],
        ["pH", str(ph)],
        ["TDS", str(tds)]
    ], colWidths=[3 * inch, 2.5 * inch])

    tabla_suelo.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            )
        ])
    )

    elementos.append(
        tabla_suelo
    )

    elementos.append(
        Spacer(1, 20)
    )

    # ============================================================
    # EVIDENCIA
    # ============================================================

    elementos.append(
        Paragraph(
            "4. Evidencia visual",
            estilos["Heading2"]
        )
    )

    elementos.append(
        Spacer(1, 8)
    )

    if archivo_imagen:

        ruta_imagen = Path(
            archivo_imagen
        )

        if ruta_imagen.exists():

            imagen = Image(
                str(ruta_imagen),
                width=5 * inch,
                height=3.5 * inch
            )

            elementos.append(
                imagen
            )

    elementos.append(
        Spacer(1, 15)
    )

    # ============================================================
    # FUENTE DE DATOS
    # ============================================================

    elementos.append(
        Paragraph(
            "Fuente de telemetría: InfluxDB",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            "Fuente de visión: YOLO",
            estilos["Normal"]
        )
    )

    elementos.append(
        Spacer(1, 10)
    )

    elementos.append(
        Paragraph(
            "Sistema AgroIA - Análisis de suelo mediante "
            "visión por computador e IoT.",
            estilos["Normal"]
        )
    )

    # ============================================================
    # GENERAR PDF
    # ============================================================

    doc.build(elementos)

    return str(ruta_salida)
