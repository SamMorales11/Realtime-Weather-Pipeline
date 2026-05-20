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
```

## 2. Konfigurasi Environment Variables
Buat file .env di direktori utama (root) proyek dan tambahkan konfigurasi berikut untuk menghubungkan API:
```bash
OPENWEATHER_API_KEY=masukkan_api_key_anda_disini
CITY_NAME=Jakarta
COUNTRY_CODE=ID
```

## 3. Instalasi Dependensi Python
Sangat disarankan menggunakan virtual environment
```bash
python -m venv venv

# Aktivasi di Windows:
venv\Scripts\activate
# Aktivasi di Mac/Linux:
source venv/bin/activate

# Instalasi semua pustaka yang dibutuhkan
pip install pandas pyarrow duckdb prefect requests python-dotenv
```

## 4. Menjalankan Pipeline & Automasi (Prefect)
4.1 Menyuntikkan Data Historis (Seeding)
Jalankan skrip ini untuk membuat mock data historis 24 jam terakhir agar Superset memiliki data awal untuk divisualisasikan secara langsung:
```bash
python src/seed_data.py
```
4.2 Menjalankan ETL Real-Time
Skrip ini akan mengaktifkan flow Prefect untuk menarik data cuaca terbaru dan memasukkannya ke data lake secara idempotent:
```bash
python src/ingestion.py
```

## 📊 Visualisasi Apache Superset
<img width="1850" height="548" alt="Screenshot 2026-05-20 093313" src="https://github.com/user-attachments/assets/44c9f048-071e-44b6-889b-9261f77e957f" />
<img width="1838" height="467" alt="Screenshot 2026-05-20 093333" src="https://github.com/user-attachments/assets/15391812-c50b-456f-99e4-41d4509914ec" />
<img width="1232" height="457" alt="Screenshot 2026-05-20 093342" src="https://github.com/user-attachments/assets/61526924-1c8e-469d-88ba-59bba4ea758b" />

Jika Anda menggunakan Docker untuk menjalankan Superset, hidupkan container dengan perintah berikut di terminal:
```bash
docker-compose up -d
```
Setelah sistem online, akses http://localhost:8088, hubungkan ke database DuckDB yang mengarah ke file Parquet kita, dan Command Center Anda siap memantau analitik cuaca secara dinamis!



