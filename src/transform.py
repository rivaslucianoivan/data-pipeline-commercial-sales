import pandas as pd

def preparar_datos_ventas(df_ecom, df_local, df_productos):
    #Normalizar e-commerce
    ecom = df_ecom.copy()
    ecom = ecom.rename(columns={
        "id_pedido": "id_documento",
    })
    # Asegurar columnas mínimas
    ecom["cliente_id"] = ecom.get("cliente_id", None)

    #Normalizar local
    local = df_local.copy()
    local = local.rename(columns={
        "id_ticket": "id_documento",
    })
    # En local no hay cliente_id; lo dejamos como NaN
    local["cliente_id"] = None

    #Concatenar
    columnas_base = [
        "fecha", "id_documento", "id_producto", "cantidad",
        "precio_unitario", "moneda", "canal", "cliente_id"
    ]
    df_raw = pd.concat(
        [ecom[columnas_base], local[columnas_base]],
        ignore_index=True
    )

    #Merge con productos
    df = df_raw.merge(
        df_productos,
        on="id_producto",
        how="left",
        validate="m:1",
    )

    #Columnas calculadas
    df["ingreso_bruto"] = df["cantidad"] * df["precio_unitario"]
    df["costo_total"] = df["cantidad"] * df["costo_unitario"]
    df["margen_bruto"] = df["ingreso_bruto"] - df["costo_total"]
    df["margen_pct"] = df["margen_bruto"] / df["ingreso_bruto"].replace(0, pd.NA)

    #Columnas de fecha derivadas
    df["anio"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["dia"] = df["fecha"].dt.date

    return df_raw, df


def generar_kpis_basicos(df_clean) -> dict:
    kpis = {}

    # Ventas por día y canal
    resumen_diario = (
        df_clean
        .groupby(["dia", "canal"], as_index=False)
        .agg({
            "ingreso_bruto": "sum",
            "margen_bruto": "sum",
            "cantidad": "sum",
        })
    )
    resumen_diario["margen_pct"] = (
        resumen_diario["margen_bruto"] / resumen_diario["ingreso_bruto"].replace(0, pd.NA)
    )
    kpis["resumen_diario"] = resumen_diario

    # Ventas por categoría
    por_categoria = (
        df_clean
        .groupby(["categoria"], as_index=False)
        .agg({
            "ingreso_bruto": "sum",
            "margen_bruto": "sum",
            "cantidad": "sum",
        })
    )
    por_categoria["margen_pct"] = (
        por_categoria["margen_bruto"] / por_categoria["ingreso_bruto"].replace(0, pd.NA)
    )
    kpis["por_categoria"] = por_categoria

    # Top productos por ingreso
    top_productos = (
        df_clean
        .groupby(["id_producto", "nombre_producto"], as_index=False)
        .agg({
            "ingreso_bruto": "sum",
            "margen_bruto": "sum",
            "cantidad": "sum",
        })
        .sort_values("ingreso_bruto", ascending=False)
        .head(20)
    )
    kpis["top_productos"] = top_productos

    return kpis

def generar_tablas_resumen(df_clean) -> dict:
    tablas = {}

    tabla_dia_canal = (
        df_clean
        .pivot_table(
            index="dia",
            columns="canal",
            values="ingreso_bruto",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )
    tablas["tabla_dia_canal"] = tabla_dia_canal

    tabla_cat_canal = (
        df_clean
        .pivot_table(
            index="categoria",
            columns="canal",
            values="ingreso_bruto",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )
    tablas["tabla_categoria_canal"] = tabla_cat_canal

    return tablas

