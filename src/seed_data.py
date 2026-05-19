import os
import pandas as pd
from datetime import datetime, timedelta
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PARQUET_FILE = PROCESSED_DIR / "weather_analytics.parquet"

def inject_historical_data():
    print("=== MEMULAI PROSES DATA SEEDING BATCH REKAYASA ===")
    
    existing_df = pd.DataFrame()
    if os.path.exists(PARQUET_FILE):
        existing_df = pd.read_parquet(PARQUET_FILE)
        print(f"Membaca {len(existing_df)} data asli.")

    mock_records = []
    now = datetime.now()
    
    print("Merekayasa tren cuaca Jakarta untuk 24 jam terakhir...")
    for i in range(24):
        target_time = now - timedelta(hours=i)
        
        hour = target_time.hour
        if 11 <= hour <= 15:
            base_temp = random.uniform(32.0, 34.5)
            humidity = random.randint(55, 65)
            desc = "broken clouds"
        elif 18 <= hour <= 22:
            base_temp = random.uniform(28.0, 30.0)
            humidity = random.randint(75, 85)
            desc = "few clouds"
        else:
            base_temp = random.uniform(26.0, 28.5)
            humidity = random.randint(80, 90)
            desc = "scattered clouds"
            
        record = {
            "data_timestamp": target_time,
            "city_id": 1642911,
            "city_name": "Jakarta",
            "country": "ID",
            "temperature": round(base_temp, 2),
            "feels_like": round(base_temp + random.uniform(5.0, 7.0), 2),
            "humidity": humidity,
            "pressure": random.randint(1008, 1012),
            "weather_main": "Clouds",
            "weather_desc": desc,
            "wind_speed": round(random.uniform(0.5, 3.5), 1),
            "extracted_at": datetime.now()
        }
        mock_records.append(record)
        
    mock_df = pd.DataFrame(mock_records)
    
    if not existing_df.empty:
        final_df = pd.concat([existing_df, mock_df], ignore_index=True)
    else:
        final_df = mock_df
        
    final_df = final_df.drop_duplicates(subset=["data_timestamp"], keep="first")
    final_df = final_df.sort_values(by="data_timestamp").reset_index(drop=True)
    
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    final_df.to_parquet(PARQUET_FILE, engine="pyarrow", index=False)
    print(f"=== SUKSES BESAR! Total data lake berisi {len(final_df)} baris. ===")

if __name__ == "__main__":
    inject_historical_data()