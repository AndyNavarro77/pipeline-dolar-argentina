# 📊 Pipeline Automatizado de Cotizaciones del Dólar — Argentina FX Monitor

> **Pipeline ETL de punta a punta que convierte la volátil información cambiaria argentina en inteligencia de negocio en tiempo real — completamente automatizado, sin intervención manual.**

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)](https://mysql.com)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi)](https://powerbi.microsoft.com)
[![Automatización](https://img.shields.io/badge/Automatización-Task%20Scheduler%20%2B%20n8n-green)]()
[![Estado](https://img.shields.io/badge/Estado-Activo-brightgreen)]()

---

## 🧠 El Problema de Negocio

Argentina opera con **7 tipos de cambio simultáneos** — cada uno con implicancias distintas para precios, contratos, importaciones y planificación financiera. La brecha entre el dólar oficial y el informal (blue) puede moverse varios puntos porcentuales en una sola semana, impactando directamente en costos, márgenes y decisiones estratégicas.

Hacer seguimiento manual de estos valores implica:
- **Alto costo operativo** — consultar múltiples fuentes todos los días
- **Riesgo de error** — capturas desactualizadas y datos copiados a mano
- **Reactividad** — las decisiones llegan *después* de que el riesgo u oportunidad ya se movió

**Este pipeline elimina ese problema.**

---

## ✅ La Solución

Un pipeline de datos completamente automatizado que extrae cotizaciones en tiempo real, las procesa, las almacena con controles de integridad y las presenta en un dashboard interactivo — con alertas proactivas cuando los valores superan umbrales críticos.

> *De datos crudos de la API a dashboard accionable en menos de 60 segundos. Se ejecuta todos los días sin intervención humana.*

---

## 📐 Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   dolarapi.com  │───▶│  Python ETL      │───▶│   MySQL DB      │
│   (API Pública) │    │  extract_dolar.py│    │  (lógica UPSERT)│
└─────────────────┘    └──────────────────┘    └────────┬────────┘
                                                         │
                              ┌──────────────────────────▼──────────┐
                              │         Dashboard Power BI           │
                              │  (KPIs en vivo · Tendencias · Spread)│
                              └─────────────────────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                           │
     ┌────────▼────────┐       ┌─────────▼──────────┐               │
     │ Task Scheduler  │       │       n8n           │               │
     │ (Ejecución diaria)      │ (Alertas por umbral)│               │
     └─────────────────┘       └────────────────────┘               │
```

---

## 🔄 Pipeline — Paso a Paso

| Paso | Acción | Tecnología | Valor de Negocio |
|------|--------|------------|------------------|
| 1 | Extracción de datos FX desde API pública | Python · requests | Datos siempre actualizados, sin consulta manual |
| 2 | Validación, limpieza y transformación | Python · pandas | Garantiza calidad y consistencia del dato |
| 3 | Simulación de histórico para análisis temporal | Python · pandas | Habilita análisis de tendencias desde el primer día |
| 4 | Carga a base de datos relacional con UPSERT | MySQL · SQL | Previene duplicados, mantiene integridad |
| 5 | Visualización interactiva y KPIs | Power BI | Insights listos para la toma de decisiones |
| 6 | Ejecución automática diaria | Windows Task Scheduler | Cero carga operativa |
| 7 | Alertas por email ante umbrales | n8n | Notificación proactiva antes del descubrimiento manual |

---

## 📊 Dashboard

El dashboard en Power BI fue diseñado para responder las preguntas que importan a quienes toman decisiones:

![Vista del Dashboard](img/image.png)

**Qué muestra:**

- **Cotizaciones de compra y venta en tiempo real** para los 7 tipos (blue, bolsa, CCL, cripto, mayorista, oficial, tarjeta)
- **Tipo de cambio actual por tipo** — gráfico de barras horizontales para comparación visual inmediata
- **Tendencia de precio de venta** — serie temporal desde marzo 2026
- **Spread informal vs. oficial (semanal)** — análisis semana a semana para detectar patrones de volatilidad
- **KPIs:** Dólar Oficial · Dólar Blue · Promedio · Spread Informal %

---

## 🔔 Automatización y Alertas

**Ejecución programada** via Windows Task Scheduler: el pipeline y el dashboard se actualizan diariamente sin ningún paso manual.

**Alertas proactivas** via flujo en n8n: cuando el dólar blue supera un umbral definido (ej: > $1.600 ARS), se dispara automáticamente una notificación por email — permitiendo actuar sobre movimientos del mercado en tiempo real, sin esperar al próximo reporte.

---

## ✉️ Prueba Real — Funciona en Producción

Este pipeline no es solo código — se ejecuta en producción todos los días. Acá la prueba:

**Reporte HTML automatizado entregado diariamente por email:**

![Reporte por Email](img/email_report.png)

**Flujo en n8n — lógica de alertas basada en eventos:**

![Flujo n8n](img/n8n_workflow.png)

> El reporte se genera y envía automáticamente tras cada ejecución exitosa del pipeline, incluyendo KPIs en vivo: Dólar Oficial, Dólar Blue, todos los tipos de cambio, Spread Informal % y total de registros procesados.

---

## 💡 Resultados y Valor Generado

| Antes | Después |
|-------|---------|
| Consulta manual diaria en múltiples fuentes | Ingesta automatizada diaria desde una sola API |
| Sin historial para análisis de tendencias | Base de datos estructurada con serie temporal completa |
| Conciencia reactiva de los movimientos | Alertas proactivas por email ante umbrales definidos |
| Snapshots estáticos sin comparación | Dashboard interactivo con comparación multi-tipo |
| Alta carga operativa | Cero intervención manual post-despliegue |

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Propósito |
|------|------------|-----------|
| Extracción | Python · requests | Consumo de API y obtención de datos crudos |
| Transformación | Python · pandas | Limpieza, tipado y deduplicación |
| Almacenamiento | MySQL 8.0 · SQL | Persistencia relacional con lógica UPSERT |
| Visualización | Power BI | Dashboard interactivo y reportes de KPIs |
| Programación | Windows Task Scheduler | Ejecución automatizada diaria |
| Alertas | n8n | Notificaciones por email basadas en eventos |

---

## 📁 Estructura del Repositorio

```
pipeline-dolar-argentina/
│
├── extract_dolar.py       # Script ETL principal — extracción, transformación y carga
├── requirements.txt       # Dependencias Python
├── .env.example           # Template de variables de entorno (sin credenciales)
├── dashboard/             # Archivo Power BI .pbix
├── data/                  # Datos históricos
├── img/                   # Capturas del dashboard y reportes
└── README.md              # Versión en inglés
```

---

## 👤 Autor

**Andrés Navarro**
Analista de Datos · BI · ETL · Python · SQL

[![GitHub](https://img.shields.io/badge/GitHub-AndyNavarro77-black?logo=github)](https://github.com/AndyNavarro77)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Conectar-blue?logo=linkedin)](https://www.linkedin.com/in/andr%C3%A9s-navarro77/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visitar-orange?logo=netlify)](https://andres-navarro-portfolio.netlify.app/)

---

*Construido para demostrar ingeniería de datos end-to-end, automatización y analítica orientada al negocio — habilidades aplicables a cualquier industria donde la frescura del dato y la eficiencia operativa sean críticas.*