import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

random.seed(42)
SALIDA = Path("data/entrada")
SALIDA.mkdir(parents=True, exist_ok=True)

CIUDADES = ["Lima", "Arequipa", "Trujillo", "Piura", "Cusco", "Chiclayo"]
PRODUCTOS = ["Cuenta de ahorro", "Tarjeta de crédito", "Préstamo personal", "Cuenta corriente"]


def generar_clientes(n, inicio_mes, mes_nombre):
    filas = []
    for i in range(n):
        fecha = inicio_mes + timedelta(days=random.randint(0, 27))
        filas.append({
            "id_cliente": f"CL{random.randint(1000, 9999)}",
            "producto": random.choice(PRODUCTOS),
            "ciudad": random.choice(CIUDADES),
            "saldo": round(random.uniform(0, 50000), 2),
            "fecha_apertura": fecha,
        })
    df = pd.DataFrame(filas)
    df["mes"] = mes_nombre
    return df


def ensuciar(df, mes):
    """Introduce errores típicos de reportes reales."""
    df = df.copy()

    # Formato de fecha distinto según el archivo
    if mes == "marzo":
        df["fecha_apertura"] = df["fecha_apertura"].apply(lambda d: d.strftime("%d/%m/%Y"))
    else:
        df["fecha_apertura"] = df["fecha_apertura"].apply(lambda d: d.strftime("%Y-%m-%d"))

    # Nombre de columna distinto en un archivo
    if mes == "febrero":
        df = df.rename(columns={"ciudad": "Ciudad"})

    # Algunos saldos llegan como texto con símbolo
    df["saldo"] = df["saldo"].astype(object)
    idx = random.sample(range(len(df)), 15)
    df.loc[idx, "saldo"] = df.loc[idx, "saldo"].apply(lambda s: f"S/ {s:,.2f}")

    # Nulos
    idx = random.sample(range(len(df)), 10)
    df.loc[idx, "producto"] = None

    # Duplicados exactos
    duplicados = df.sample(8, random_state=1)
    df = pd.concat([df, duplicados], ignore_index=True)

    return df


meses = [
    (date(2026, 1, 1), "enero"),
    (date(2026, 2, 1), "febrero"),
    (date(2026, 3, 1), "marzo"),
]

for inicio, nombre in meses:
    df = generar_clientes(300, inicio, nombre)
    df = ensuciar(df, nombre)
    archivo = SALIDA / f"clientes_{nombre}_2026.xlsx"
    df.to_excel(archivo, index=False)
    print(f"Creado: {archivo} ({len(df)} filas)")