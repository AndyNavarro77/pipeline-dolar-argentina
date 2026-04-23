# 📊 Automated Dollar Exchange Rate Data Pipeline (Argentina)

## 🚀 Project Overview

This project showcases the design and implementation of an automated ETL pipeline to extract, process, store, and visualize exchange rate data in Argentina.

It integrates multiple industry-standard tools, simulating a real-world workflow for Data Analysts and Business Intelligence roles.

---

## 🧠 Business Objective

Build a solution to:

- Monitor exchange rate trends over time  
- Compare different dollar exchange types  
- Automate data ingestion and updates  
- Trigger alerts based on business rules  
- Enable data-driven decision making  

---

## ⚙️ Tech Stack

- **Python** (pandas, requests)
- **MySQL** (data storage)
- **Power BI** (data visualization)
- **Task Scheduler** (automation)
- **n8n** (automated alerts)
- **SQL**

---

## 🔄 Data Pipeline

1. Extract data from a public API  
2. Transform and clean data using Python  
3. Simulate historical data for time-series analysis  
4. Load into MySQL with UPSERT logic  
5. Build interactive dashboards in Power BI  
6. Automate execution with Task Scheduler  
7. Send alert notifications via n8n  

---

## 📊 Dashboard Features

- Live Quotes — Buy & Sell 
- Current Rate by Type
- Sell Price Trend by Exchange Type
- Informal Spread vs Oficial
- Key performance indicators (KPIs):
  - Average
  - Blue Rate
  - Oficial Rate
  - Informal Spread

---

## 🔔 Automation & Alerts

The pipeline runs automatically on a daily basis, ensuring up-to-date data without manual intervention.

Additionally, an alert system was implemented using n8n to send email notifications when defined thresholds are exceeded.

---

## 📸 Dashboard Preview

![Dashboard](docs/dashboard_preview.png)

---

## 💡 Project Value

This project demonstrates:

- End-to-end ETL pipeline development  
- Integration across multiple tools and technologies  
- Data automation workflows  
- Time-series data modeling  
- Business-oriented analytics  

---

## 👤 Author

Andrés Navarro
