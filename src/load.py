from pathlib import Path
import pandas as pd


def asegurar_directorio_salida(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)


def exportar_a_excel(df_raw, df_clean, kpis: dict, tablas: dict, output_path) -> None:
    from pathlib import Path
    output_path = Path(output_path)
    asegurar_directorio_salida(output_path.parent)

    with pd.ExcelWriter(output_path, engine="xlsxwriter", datetime_format="yyyy-mm-dd") as writer:
        # 1) Hoja raw
        sheet_name = "raw"
        df_raw.to_excel(writer, sheet_name=sheet_name, index=False)
        ws = writer.sheets[sheet_name]
        _formatear_hoja_basica(ws, df_raw)

        # 2) Hoja clean
        sheet_name = "clean"
        df_clean.to_excel(writer, sheet_name=sheet_name, index=False)
        ws = writer.sheets[sheet_name]
        _formatear_hoja_basica(ws, df_clean)

        # 3) Hojas de KPIs
        for nombre, df_kpi in kpis.items():
            sheet_name = f"kpi_{nombre}"
            df_kpi.to_excel(writer, sheet_name=sheet_name, index=False)
            ws = writer.sheets[sheet_name]
            _formatear_hoja_basica(ws, df_kpi)

        # 4) Hojas de tablas resumen
        for nombre, df_tab in tablas.items():
            sheet_name = f"tbl_{nombre}"
            df_tab.to_excel(writer, sheet_name=sheet_name, index=False)
            ws = writer.sheets[sheet_name]
            _formatear_hoja_basica(ws, df_tab)


def _formatear_hoja_basica(worksheet, df):
    # Freeze panes: fila 1 (index 0 es encabezado, se congela debajo)
    worksheet.freeze_panes(1, 0)  # congela la primera fila[web:176][web:187]

    # Autofiltro en la fila de encabezados
    num_cols = len(df.columns)
    if num_cols > 0:
        worksheet.autofilter(0, 0, 0, num_cols - 1)  # solo encabezado[web:176][web:178]

    # Ajuste de ancho de columnas (simple)
    for idx, col in enumerate(df.columns):
        serie = df[col].astype(str)
        max_len = max(serie.map(len).max(), len(str(col))) + 2
        if max_len > 50:
            max_len = 50
        worksheet.set_column(idx, idx, max_len)
