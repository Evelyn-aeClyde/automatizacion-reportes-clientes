import sqlite3
from pathlib import Path

import pandas as pd

ENTRADA = Path("data/entrada")
SALIDA_DB = Path("data/clientes.db")
SALIDA_XLSX = Path("reportes/consolidado.xlsx")


def cargar_archivo(ruta):
    df = pd.read_excel(ruta)
    # Unifica nombres de columna distintos entre archivos
    df.columns = [c.lower() for c in df.columns]
    return df


def limpiar_saldo(serie):
    return (
        serie.astype(str)
        .str.replace("S/", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .astype(float)
    )


def limpiar_fecha(serie):
    # Intenta dos formatos distintos: AAAA-MM-DD y DD/MM/AAAA
    fechas = pd.to_datetime(serie, format="%Y-%m-%d", errors="coerce")
    faltantes = fechas.isnull()
    fechas[faltantes] = pd.to_datetime(serie[faltantes], format="%d/%m/%Y", errors="coerce")
    return fechas


def agregar_grafico(ruta_excel):
    from openpyxl import load_workbook
    from openpyxl.chart import BarChart, Reference

    wb = load_workbook(ruta_excel)
    ws = wb["Por producto"]

    chart = BarChart()
    chart.title = "Saldo total por producto"
    chart.y_axis.title = "Saldo total (S/)"
    chart.x_axis.title = "Producto"

    num_filas = ws.max_row
    datos = Reference(ws, min_col=3, min_row=1, max_row=num_filas)
    categorias = Reference(ws, min_col=1, min_row=2, max_row=num_filas)
    chart.add_data(datos, titles_from_data=True)
    chart.set_categories(categorias)

    ws.add_chart(chart, "F2")
    wb.save(ruta_excel)


def main():
    archivos = sorted(ENTRADA.glob("clientes_*_2026.xlsx"))
    print(f"Archivos encontrados: {len(archivos)}")

    dfs = [cargar_archivo(a) for a in archivos]
    df = pd.concat(dfs, ignore_index=True)
    print("Filas antes de limpiar:", len(df))

    df["saldo"] = limpiar_saldo(df["saldo"])
    df["fecha_apertura"] = limpiar_fecha(df["fecha_apertura"])

    nulos_producto = df["producto"].isnull().sum()
    print("Registros con producto nulo:", nulos_producto)
    df["producto"] = df["producto"].fillna("Sin especificar")

    antes = len(df)
    df = df.drop_duplicates()
    print(f"Duplicados eliminados: {antes - len(df)}")
    print("Filas finales:", len(df))

    SALIDA_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(SALIDA_DB)
    df.to_sql("clientes", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Base de datos guardada en {SALIDA_DB}")

    SALIDA_XLSX.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(SALIDA_XLSX, index=False)
    print(f"Excel consolidado guardado en {SALIDA_XLSX}")

    # Reporte con resúmenes y gráfico
    resumen_producto = (
        df.groupby("producto")
        .agg(num_clientes=("id_cliente", "count"), saldo_total=("saldo", "sum"), saldo_promedio=("saldo", "mean"))
        .round(2)
        .reset_index()
        .sort_values("saldo_total", ascending=False)
    )
    resumen_ciudad = (
        df.groupby("ciudad")
        .agg(num_clientes=("id_cliente", "count"), saldo_total=("saldo", "sum"))
        .round(2)
        .reset_index()
        .sort_values("saldo_total", ascending=False)
    )

    reporte_path = Path("reportes/resumen.xlsx")
    with pd.ExcelWriter(reporte_path, engine="openpyxl") as writer:
        resumen_producto.to_excel(writer, sheet_name="Por producto", index=False)
        resumen_ciudad.to_excel(writer, sheet_name="Por ciudad", index=False)
        df.to_excel(writer, sheet_name="Datos completos", index=False)

    agregar_grafico(reporte_path)
    print(f"Reporte con resumen guardado en {reporte_path}")


if __name__ == "__main__":
    main()
