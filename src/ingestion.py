import os
import requests
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from prefect import task, flow

# Import fungsi transformasi dari file sebelah
from transformation import transform_and_save_parquet

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

def get_api_config():
    return {
        "API_KEY": os.getenv("OPENWEATHER_API_KEY"),
        "CITY": os.getenv("CITY_NAME", "Jakarta")
    }

@task(retries=3, retry_delay_seconds=60, name="Fetch Weather From API")
def fetch_weather_data():
    config = get_api_config()
    api_key = config["API_KEY"]
    city = config["CITY"]

    if not api_key:
        raise ValueError("API Key tidak ditemukan! Periksa kembali file .env Anda.")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    logging.info(f"Memulai pengambilan data cuaca untuk kota: {city}")
    response = requests.get(url, timeout=10)
    response.raise_for_status() 
    return response.json()

@task(name="Save Raw JSON Data")
def save_raw_data(data):
    if not data:
        return
    config = get_api_config()
    city = config["CITY"]
    
    raw_dir = BASE_DIR / "data" / "raw"
    os.makedirs(raw_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = raw_dir / f"weather_{city}_{timestamp}.json"
    
    import json
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    
    logging.info(f"Data mentah berhasil disimpan di: {file_path}")
    return str(file_path)

# Kita bungkus fungsi transformasi lama menjadi Prefect Task resmi
@task(name="Transform JSON to Idempotent Parquet")
def transform_task():
    logging.info("Memulai proses transformasi data lake...")
    transform_and_save_parquet()

@flow(name="End-to-End Weather Data Pipeline")
def weather_pipeline():
    """
    Main Flow tunggal yang mengontrol seluruh siklus data:
    Fetch API -> Simpan Raw -> Transformasi ke Parquet.
    """
    try:
        raw_data = fetch_weather_data()
        save_raw_data(raw_data)
        
        # Jalankan transformasi langsung setelah data mentah aman
        transform_task()
        
    except Exception as e:
        logging.error(f"Pipeline gagal dieksekusi: {e}")

if __name__ == "__main__":
    weather_pipeline()