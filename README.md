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

## Stack técnico

- **Python 3.x**
- **pandas** para lectura y manipulación de datos (CSV / Excel)[web:90][web:96]
- **openpyxl** / **xlsxwriter** para leer y escribir archivos `.xlsx` con formato[web:6][web:104]
- **python-dotenv** para manejar configuración (rutas de archivos, etc.)
- **schedule** (opcional) para programar la ejecución automática del pipeline

---

## Estructura del repositorio (planificada)

```text
data-pipeline-commercial-sales/
├─ src/
│  ├─ extract.py      # Lectura de datasets (productos, ventas e‑commerce, ventas local)
│  ├─ transform.py    # Limpieza, unificación, creación de KPIs
│  ├─ load.py         # Generación del Excel final
│  └─ pipeline.py     # Orquestador ETL de punta a punta
├─ data/
│  ├─ raw/            # Archivos de entrada (CSV / Excel) de ejemplo
│  └─ processed/      # Datos intermedios (opcional)
├─ output/            # Reportes generados (reporte_ventas_semanal.xlsx)
├─ notebooks/         # Análisis exploratorios y pruebas (EDA)
├─ .gitignore
├─ requirements.txt
└─ README.md
