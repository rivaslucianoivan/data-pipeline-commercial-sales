# data-pipeline-commercial-sales

Proyecto de portafolio para construir un **pipeline ETL** que toma datos de ventas comerciales desde múltiples fuentes (e‑commerce y punto de venta físico), los limpia con **Python + pandas** y genera un **reporte automatizado en Excel** listo para usuarios de negocio.[web:101][web:95]

---

## Objetivos del proyecto

- Practicar diseño de pipelines **ETL** sobre archivos (CSV / Excel).[web:91][web:103]
- Unificar ventas de canal online y local en un único modelo tabular.
- Calcular KPIs de negocio: ingresos, márgenes, top productos, ventas por canal y por fecha.
- Generar un archivo `reporte_ventas_semanal.xlsx` con varias hojas:
  - Datos originales (`raw`)
  - Datos limpios y unificados
  - Hojas de KPIs y tablas tipo dinámica

---

## Como ejecutarlo:

### 1. Activar entorno virtual
.\.venv\Scripts\activate  # Windows CMD/PowerShell

### 2. Instalar dependencias
pip install -r requirements.txt

### 3. Ejecutar pipeline
python -m src.pipeline

---


## Stack técnico

- **Python 3.x**
- **pandas** para lectura y manipulación de datos (CSV / Excel)[web:90][web:96]
- **openpyxl** / **xlsxwriter** para leer y escribir archivos `.xlsx` con formato[web:6][web:104]
- **python-dotenv** para manejar configuración (rutas de archivos, etc.)
- **schedule** (opcional) para programar la ejecución automática del pipeline

---

## Estructura del repositorio 

```text
data-pipeline-commercial-sales/
├── src/
│   ├── __init__.py
│   ├── extract.py      # Lectura de datos CSV/Excel
│   ├── transform.py    # Unificación, limpieza, KPIs
│   ├── load.py         # Exportación a Excel con formato
│   └── pipeline.py     # Orquestador ETL
├── data/
│   └── raw/            # Datasets de ejemplo
│       ├── productos.xlsx
│       ├── ventas_ecommerce.csv
│       └── ventas_local.csv
├── output/             # Reportes generados
├── logs/               # Logs de ejecución
├── notebooks/          # (Opcional) EDA y pruebas
├── .gitignore
├── requirements.txt
└── README.md

