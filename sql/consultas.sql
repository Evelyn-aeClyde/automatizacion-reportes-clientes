-- 1. Saldo total y promedio por producto
SELECT producto,
    COUNT(*) AS num_clientes,
    ROUND(SUM(saldo), 2) AS saldo_total,
    ROUND(AVG(saldo), 2) AS saldo_promedio
FROM clientes
GROUP BY producto
ORDER BY saldo_total DESC;

-- 2. Clientes por ciudad
SELECT ciudad, COUNT(*) AS num_clientes
FROM clientes
GROUP BY ciudad
ORDER BY num_clientes DESC;

-- 3. Clientes por mes de apertura
SELECT strftime('%Y-%m', fecha_apertura) AS mes,
    COUNT(*) AS aperturas
FROM clientes
GROUP BY mes
ORDER BY mes;

-- 4. Top 10 clientes por saldo
SELECT id_cliente, producto, ciudad, saldo
FROM clientes
ORDER BY saldo DESC
LIMIT 10;

-- 5. Clientes con saldo menor a 1000 (posible oportunidad de activación)
SELECT COUNT(*) AS clientes_saldo_bajo
FROM clientes
WHERE saldo < 1000;

-- 6. Saldo promedio por ciudad y producto
SELECT ciudad, producto, ROUND(AVG(saldo), 2) AS saldo_promedio
FROM clientes
GROUP BY ciudad, producto
ORDER BY ciudad, saldo_promedio DESC;

for nombre, query in [
    ("Por producto", "SELECT producto, COUNT(*) n, ROUND(AVG(saldo),2) saldo_prom FROM clientes GROUP BY producto"),
    ("Por ciudad", "SELECT ciudad, COUNT(*) n FROM clientes GROUP BY ciudad ORDER BY n DESC"),
]:
    print(f"\n{nombre}:")
    print(pd.read_sql(query, conn))