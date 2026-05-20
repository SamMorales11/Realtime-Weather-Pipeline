```markdown
# Real-Time Weather Data Pipeline & Analytics 🌦️

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Prefect](https://img.shields.io/badge/Orchestration-Prefect%203.0-brightgreen.svg?logo=prefect&logoColor=white)](https://www.prefect.io/)
[![DuckDB](https://img.shields.io/badge/Analytics-DuckDB-orange.svg?logo=duckdb&logoColor=white)](https://duckdb.org/)
[![Apache Superset](https://img.shields.io/badge/BI%20Dashboard-Apache%20Superset-red.svg?logo=apachesuperset&logoColor=white)](https://superset.apache.org/)

Repositori ini berisi infrastruktur data pipeline *end-to-end* yang mengekstraksi data cuaca secara *real-time* dari OpenWeather API untuk wilayah Jakarta, mengorkestrasikannya menggunakan **Prefect**, menyimpan data dalam format *columnar storage* (**Parquet** & **DuckDB**), serta memvisualisasikannya ke dalam dashboard analitik interaktif **Apache Superset**.

Proyek ini dirancang dengan standar *enterprise-level data stack* yang mengutamakan idempotensi, performa kueri analitik tinggi, serta pemisahan arsitektur yang bersih.

---

## 📌 Arsitektur Sistem

Pipeline ini menggunakan pendekatan *Modern Data Stack* (MDS) ringan untuk menangani data aliran (*streaming/frequent batch*):

[OpenWeather API] ──(Ingestion via Python)──> [Prefect Core]
                                                   │
                                            (Data Transformation)
                                                   │
                                                   ▼
                                      [Local Parquet Data Lake]
                                                   │
                                         (Analytical Queries)
                                                   ▼
                                              [DuckDB Engine]
                                                   │
                                                   ▼
                                      [Apache Superset Dashboard]
