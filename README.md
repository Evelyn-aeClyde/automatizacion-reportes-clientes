# Automatización de reportes de clientes

Script que consolida reportes mensuales de clientes con errores típicos de datos reales (columnas con nombres distintos, fechas en formatos mixtos, saldos como texto, duplicados y valores nulos), limpia la información y genera una base de datos y un reporte en Excel con tablas y gráfico.

## Problema

Cada mes llegan reportes de clientes en archivos Excel separados, con inconsistencias de formato entre ellos. ¿Cómo unificarlos, limpiarlos y generar un reporte consolidado de forma automática y repetible?

## Datos

Los datos son **sintéticos**, generados con `generar_datos.py` para simular tres reportes mensuales (enero, febrero y marzo de 2026) con errores típicos de reportes reales:

- Nombre de columna distinto entre archivos (`ciudad` vs `Ciudad`).
- Fechas en dos formatos (`AAAA-MM-DD` y `DD/MM/AAAA`).
- Saldos guardados como texto con símbolo de moneda (`S/ 22,453.34`).
- Valores nulos en el campo producto.
- Filas duplicadas.

No contienen información de ningún banco ni cliente real.

## Metodología

1. **Generación:** `generar_datos.py` crea 3 archivos Excel (~300 filas cada uno) con los errores descritos.
2. **Consolidación:** `consolidar.py` lee los 3 archivos, unifica nombres de columna, limpia saldos y fechas, imputa nulos en producto como "Sin especificar" y elimina duplicados.
3. **Almacenamiento:** los datos limpios se guardan en SQLite (`data/clientes.db`) y en un Excel plano (`reportes/consolidado.xlsx`).
4. **Consultas SQL:** `sql/consultas.sql` contiene 6 consultas documentadas (saldo por producto, clientes por ciudad, aperturas por mes, top 10 por saldo, clientes de saldo bajo, saldo por ciudad y producto).
5. **Reporte final:** `consolidar.py` genera `reportes/resumen.xlsx` con tres pestañas (Por producto, Por ciudad, Datos completos) y un gráfico de barras del saldo total por producto.

## Resultados

- 924 registros combinados de los 3 archivos mensuales.
- 30 registros con producto nulo, imputados como "Sin especificar".
- 24 filas duplicadas eliminadas.
- 900 registros finales, limpios y consolidados.

## Cómo ejecutarlo

1. Clona el repositorio.
2. Crea un entorno virtual e instala dependencias: `pip install -r requirements.txt`
3. Genera los datos de ejemplo: `python generar_datos.py`
4. Ejecuta la consolidación: `python consolidar.py`
5. Revisa las consultas SQL: `python ejecutar_consultas.py`
6. Abre `reportes/resumen.xlsx` para ver el reporte final con gráfico.

## Estructura

- `generar_datos.py`: genera 3 Excel mensuales con errores típicos.
- `consolidar.py`: lee, limpia, consolida y genera base de datos y reportes.
- `ejecutar_consultas.py`: ejecuta las consultas SQL y muestra los resultados.
- `sql/consultas.sql`: consultas documentadas sobre la base consolidada.
- `data/entrada/`: archivos Excel mensuales (generados por el script).
- `reportes/`: Excel consolidado y reporte con gráfico.