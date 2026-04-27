-- ============================================================
-- Argentina FX Monitor — Database Schema
-- Author: Andrés Navarro
-- GitHub: https://github.com/AndyNavarro77/pipeline-dolar-argentina
-- ============================================================

-- Create and select database
CREATE DATABASE IF NOT EXISTS pipeline_dolar
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE pipeline_dolar;

-- ============================================================
-- TABLE: dolar
-- Main FX rates table. Records are upserted on each pipeline
-- run — duplicates are prevented via the composite unique key.
-- ============================================================
CREATE TABLE IF NOT EXISTS dolar (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    tipo_dolar      VARCHAR(50)         NOT NULL,
    nombre          VARCHAR(100)        NOT NULL,
    precio_compra   DECIMAL(10, 2),
    precio_venta    DECIMAL(10, 2),
    fecha           DATETIME            NOT NULL,
    created_at      TIMESTAMP           DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_tipo_fecha (tipo_dolar, fecha)
);

-- ============================================================
-- USEFUL QUERIES
-- ============================================================

-- Latest rate for each exchange type
-- SELECT tipo_dolar, nombre, precio_compra, precio_venta, fecha
-- FROM dolar
-- WHERE fecha = (SELECT MAX(fecha) FROM dolar)
-- ORDER BY precio_venta DESC;

-- Informal spread vs official rate (latest)
-- SELECT
--     MAX(CASE WHEN tipo_dolar = 'blue' THEN precio_venta END) AS blue,
--     MAX(CASE WHEN tipo_dolar = 'oficial' THEN precio_venta END) AS oficial,
--     ROUND(
--         (MAX(CASE WHEN tipo_dolar = 'blue' THEN precio_venta END) -
--          MAX(CASE WHEN tipo_dolar = 'oficial' THEN precio_venta END)) /
--          MAX(CASE WHEN tipo_dolar = 'oficial' THEN precio_venta END) * 100, 2
--     ) AS spread_pct
-- FROM dolar
-- WHERE fecha = (SELECT MAX(fecha) FROM dolar);

-- Weekly blue rate trend
-- SELECT
--     YEARWEEK(fecha) AS week,
--     AVG(precio_venta) AS avg_blue
-- FROM dolar
-- WHERE tipo_dolar = 'blue'
-- GROUP BY YEARWEEK(fecha)
-- ORDER BY week DESC
-- LIMIT 8;

-- All rate types sorted by sell price (latest snapshot)
-- SELECT tipo_dolar, nombre, precio_compra, precio_venta
-- FROM dolar
-- WHERE fecha = (SELECT MAX(fecha) FROM dolar)
-- ORDER BY precio_venta DESC;