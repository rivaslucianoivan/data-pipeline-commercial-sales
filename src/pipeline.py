import logging
from pathlib import Path
from datetime import datetime
from time import perf_counter
from src.extract import (
    cargar_config_rutas,
    leer_productos,
    leer_ventas_ecommerce,
    leer_ventas_local,
)
from src.transform import (
    preparar_datos_ventas,
    generar_kpis_basicos,
    generar_tablas_resumen,
)
from src.load import exportar_a_excel

def setup_logging() -> logging.Logger:
    logs_dir = Path(__file__).resolve().parents[1] / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_path = logs_dir / f"pipeline_{datetime.now().strftime('%Y%m%d')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ],
    )

    logger = logging.getLogger("sales_pipeline")
    return logger

def run_pipeline() -> None:
    logger = setup_logging()
    logger.info("Starting sales Excel pipeline")

    t0 = perf_counter()

    try:
        #Config
        paths = cargar_config_rutas()
        logger.info(f"Using raw data from: {paths['productos'].parent}")

        #Extract
        df_prod = leer_productos(paths["productos"])
        df_ecom = leer_ventas_ecommerce(paths["ventas_ecommerce"])
        df_local = leer_ventas_local(paths["ventas_local"])

        logger.info(f"Products loaded: {len(df_prod)}")
        logger.info(f"E-commerce rows loaded: {len(df_ecom)}")
        logger.info(f"Local POS rows loaded: {len(df_local)}")

        #Transform
        df_raw, df_clean = preparar_datos_ventas(df_ecom, df_local, df_prod)
        logger.info(f"Unified raw rows: {len(df_raw)}")
        logger.info(f"Clean rows after enrichment: {len(df_clean)}")

        sanity_check(df_clean)
        kpis = generar_kpis_basicos(df_clean)
        tablas = generar_tablas_resumen(df_clean)
        logger.info(
            "Generated KPI tables: %s",
            ", ".join(kpis.keys()) if kpis else "none",
        )
        logger.info(
            "Generated summary tables: %s",
            ", ".join(tablas.keys()) if tablas else "none",
        )

        #Load
        output_path = paths["output_dir"] / "reporte_ventas_semanal.xlsx"
        exportar_a_excel(df_raw, df_clean, kpis, tablas, output_path)
        logger.info(f"Excel report written to: {output_path}")

    except Exception as exc:
        logger.exception(f"Pipeline failed: {exc}")
        # volver a lanzar la excepción para que un scheduler lo marque como error
        raise
    finally:
        elapsed = perf_counter() - t0
        logger.info(f"Pipeline finished in {elapsed:.2f} seconds")
        
def sanity_check(df_clean) -> None:
    if df_clean.empty:
        raise ValueError("Clean dataset is empty. Aborting export.")

    if df_clean["ingreso_bruto"].sum() <= 0:
        raise ValueError("Total revenue is zero or negative. Check input data.")
        

if __name__ == "__main__":
    run_pipeline()
