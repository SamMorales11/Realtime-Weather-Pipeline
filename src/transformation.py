import os
import json
import glob
import logging
from pathlib import Path
import pandas as pd
from datetime import datetime

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Gunakan Path Absolut agar aman dari mana pun skrip dipanggil
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PARQUET_FILE = PROCESSED_DIR / "weather_analytics.parquet"

def flatten_weather_data(json_data):
    """Mengubah struktur JSON bersarang menjadi DataFrame baris tunggal."""
    try:
        flattened = {
            "data_timestamp": datetime.fromtimestamp(json_data.get("dt")),
            "city_id": json_data.get("id"),
            "city_name": json_data.get("name"),
            "country": json_data.get("sys", {}).get("country"),
            "temperature": json_data.get("main", {}).get("temp"),
            "feels_like": json_data.get("main", {}).get("feels_like"),
            "humidity": json_data.get("main", {}).get("humidity"),
            "pressure": json_data.get("main", {}).get("pressure"),
            "weather_main": json_data.get("weather", [{}])[0].get("main"),
            "weather_desc": json_data.get("weather", [{}])[0].get("description"),
            "wind_speed": json_data.get("wind", {}).get("speed"),
            "extracted_at": datetime.now()
        }
        return pd.DataFrame([flattened])
    except Exception as e:
        logging.error(f"Gagal melakukan flattening data: {e}")
        return None

def transform_and_save_parquet():
    """Membaca JSON mentah, transformasi, dan simpan ke Parquet (Idempotent)."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Cari semua file .json di folder raw secara absolut
    search_path = os.path.join(RAW_DIR, "*.json")
    json_files = glob.glob(search_path)
    
    if not json_files:
        logging.warning(f"Tidak ada file JSON mentah yang ditemukan di {RAW_DIR}")
        return

    logging.info(f"Ditemukan {len(json_files)} file JSON mentah. Memulai proses...")
    
    all_dfs = []
    for file_path in json_files:
        with open(file_path, "r") as f:
            data = json.load(f)
            df = flatten_weather_data(data)
            if df is not None:
                all_dfs.append(df)

    if not all_dfs:
        logging.warning("Tidak ada data yang berhasil di-flatten.")
        return

    new_data_df = pd.concat(all_dfs, ignore_index=True)

    # Mekanisme Idempotency (Anti-Duplikat)
    if os.path.exists(PARQUET_FILE):
        logging.info("File Parquet master ditemukan. Memeriksa duplikasi data...")
        existing_df = pd.read_parquet(PARQUET_FILE)
        combined_df = pd.concat([existing_df, new_data_df], ignore_index=True)
        final_df = combined_df.drop_duplicates(subset=["data_timestamp"], keep="first")
        rows_added = len(final_df) - len(existing_df)
        logging.info(f"Selesai menyaring. {rows_added} data baru masuk ke master.")
    else:
        logging.info("File Parquet master belum ada. Membuat file baru...")
        final_df = new_data_df.drop_duplicates(subset=["data_timestamp"], keep="first")

    # Simpan ke Parquet
    final_df.to_parquet(PARQUET_FILE, engine="pyarrow", index=False)
    logging.info(f"Data lake sukses diperbarui di: {PARQUET_FILE}")

# PASTIKAN bagian ini tertulis dengan benar di paling bawah file
if __name__ == "__main__":
    print("=== SKRIP TRANSFORMATION DIAGN_START ===")
    transform_and_save_parquet()
    print("=== SKRIP TRANSFORMATION DIAGN_END ===")