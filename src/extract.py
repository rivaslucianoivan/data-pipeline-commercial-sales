import pandas as pd
from pathlib import Path

def leer_productos(path: str) -> pd.DataFrame:
    if path.endswith('.csv'):
        df = pd.read_excel(path, encoding='utf-8')
    else:
        df = pd.read_excel(path)
    # Normalizar nombres de columnas por si Excel los cambia
    df.columns = [c.strip().lower() for c in df.columns]

    # Asegurar tipos básicos
    df['id_producto'] = df['id_producto'].astype(str)
    df['costo_unitario'] = pd.to_numeric(df['costo_unitario'])
    df['precio_lista'] = pd.to_numeric(df['precio_lista'])
    df['activo'] = df['activo'].astype(bool)

    return df


def leer_ventas_ecommerce(path: str) -> pd.DataFrame:
    if path.endswith('.csv'):
        df = pd.read_excel(path, encoding='utf-8')
    else:
        df = pd.read_excel(path)
    # Normalizar nombres
    df.columns = [c.strip().lower() for c in df.columns]

    # Tipos
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['id_pedido'] = df['id_pedido'].astype(str)
    df['id_producto'] = df['id_producto'].astype(str)
    df['cantidad'] = pd.to_numeric(df['cantidad'])
    df['precio_unitario'] = pd.to_numeric(df['precio_unitario'])

    # Asegurar columna canal, si esta columna ya existe entonces rellena las celas vacias con 'ecommerce'
    if 'canal' not in df.columns:
        df['canal'] = 'ecommerce'
    else:
        df['canal'] = df['canal'].fillna('ecommerce')

    return df


import pandas as pd

def leer_ventas_local(path: str) -> pd.DataFrame:
    if path.endswith('.csv'):
        df = pd.read_excel(path, encoding='utf-8')
    else:
        df = pd.read_excel(path)

    df.columns = [c.strip().lower() for c in df.columns]

    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['id_ticket'] = df['id_ticket'].astype(str)
    df['id_producto'] = df['id_producto'].astype(str)
    df['cantidad'] = pd.to_numeric(df['cantidad'])
    df['precio_unitario'] = pd.to_numeric(df['precio_unitario'])

    if 'canal' not in df.columns:
        df['canal'] = 'local'
    else:
        df['canal'] = df['canal'].fillna('local')

    return df


def validar_archivo(path: str) -> None:
    if not Path(path).exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")


def cargar_config_rutas() -> dict:
    base_dir = Path(__file__).resolve().parents[1]  # carpeta raíz del proyecto
    data_raw = base_dir / "data" / "raw"
    output_dir = base_dir / "output"

    return {
        "productos": data_raw / "productos.xlsx",          # o productos.csv
        "ventas_ecommerce": data_raw / "ventas_ecommerce.csv",
        "ventas_local": data_raw / "ventas_local.csv",
        "output_dir": output_dir,
    }