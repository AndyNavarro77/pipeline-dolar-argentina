# 📊 Pipeline Automatizado de Cotizaciones del Dólar (Argentina)

## 🚀 Descripción del Proyecto

Este proyecto consiste en el desarrollo de un pipeline ETL automatizado que permite la extracción, transformación, almacenamiento y visualización de datos de cotizaciones del dólar en Argentina.

El sistema integra múltiples herramientas utilizadas en entornos profesionales, simulando un flujo de trabajo real de un Analista de Datos o Business Intelligence.

---

## 🧠 Objetivo de Negocio

Desarrollar una solución que permita:

- Monitorear la evolución del dólar en el tiempo
- Comparar distintos tipos de cambio
- Automatizar la actualización de datos
- Generar alertas ante eventos relevantes
- Facilitar la toma de decisiones basada en datos

---

## ⚙️ Tecnologías Utilizadas

- **Python** (pandas, requests)
- **MySQL** (almacenamiento de datos)
- **Power BI** (visualización y análisis)
- **Task Scheduler** (automatización)
- **n8n** (alertas automatizadas)
- **SQL** (gestión y control de datos)

---

## 🔄 Flujo del Pipeline

1. Extracción de datos desde API pública  
2. Transformación y limpieza con Python  
3. Simulación de datos históricos para análisis temporal  
4. Carga en MySQL con control de duplicados (UPSERT)  
5. Visualización en Power BI  
6. Automatización diaria del pipeline  
7. Envío de alertas por email mediante n8n  

---

## 📊 Dashboard

El dashboard desarrollado permite:

- Evolución histórica del precio de venta desde marzo
- Comparación visual del precio de venta actual de cada tipo
- Tabla con cotizacion de compra y venta
- Muestra semana a semana cómo evolucionó la brecha blue/oficial
- Visualización de indicadores clave (KPIs):
  - Dolar Oficial
  - Dolar Blue
  - Dolar promedio
  - Spread Informal

---

## 🔔 Automatización y Alertas

El pipeline se ejecuta automáticamente mediante Task Scheduler, garantizando datos actualizados sin intervención manual.

Además, se implementó un sistema de alertas con n8n que envía notificaciones cuando se alcanzan ciertos umbrales (ej: dólar blue > $1600).

---

## 📸 Vista del Dashboard

![Dashboard](docs/dashboard_preview.png)

---

## 💡 Valor del Proyecto

Este proyecto demuestra:

- Construcción de pipelines ETL end-to-end  
- Integración de múltiples herramientas  
- Automatización de procesos de datos  
- Modelado para análisis temporal  
- Enfoque orientado a negocio  

---

## 👤 Autor

Andrés Navarro
