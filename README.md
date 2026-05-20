# 🌤️ Real-Time Weather Data Pipeline & Analytics

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Prefect](https://img.shields.io/badge/Orchestration-Prefect%203.0-brightgreen.svg?logo=prefect&logoColor=white)](https://www.prefect.io/)
[![DuckDB](https://img.shields.io/badge/Analytics-DuckDB-orange.svg?logo=duckdb&logoColor=white)](https://duckdb.org/)
[![Apache Superset](https://img.shields.io/badge/BI%20Dashboard-Apache%20Superset-red.svg?logo=apachesuperset&logoColor=white)](https://superset.apache.org/)

Repositori ini berisi infrastruktur *data pipeline end-to-end* untuk mengekstraksi data cuaca Jakarta secara *real-time* dari OpenWeather API. Sistem ini diorkestrasi menggunakan **Prefect**, disimpan dalam format *columnar* (**Parquet** & **DuckDB**), dan divisualisasikan menjadi *Command Center* interaktif melalui **Apache Superset**.

Proyek ini dirancang dengan standar *Modern Data Stack* (MDS) yang mengutamakan performa kueri analitik tinggi, idempotensi, dan arsitektur yang terstruktur.

---

## 🏗️ Arsitektur Sistem & Tech Stack

* **Data Ingestion & API:** Python + Requests (OpenWeather API)
* **Orchestration & Scheduling:** Prefect
* **Storage & Query Engine:** Apache Arrow (Parquet) + DuckDB
* **Business Intelligence (BI):** Apache Superset

---

## ⚙️ Prasyarat Lingkungan

Sebelum menjalankan proyek ini, pastikan sistem Anda telah terpasang:
* **Python 3.11+**
* **Docker & Docker Compose** (Opsional, sangat disarankan untuk menjalankan Apache Superset dengan mudah)
* **Git**

---

## 🛠️ Langkah-langkah Pengaturan

**1. Kloning Repositori**
```bash
git clone [https://github.com/SamMorales11/Realtime-Weather-Pipeline.git](https://github.com/SamMorales11/Realtime-Weather-Pipeline.git)
cd Realtime-Weather-Pipeline
