import os
import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
from dotenv import load_dotenv
from prefect import task, flow

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

JAKARTA_REGIONS = {
    "Jakarta Pusat": {"lat": -6.1805, "lon": 106.8284},
    "Jakarta Selatan": {"lat": -6.2615, "lon": 106.8106},
    "Jakarta Barat": {"lat": -6.1683, "lon": 106.7588},
    "Jakarta Utara": {"lat": -6.1214, "lon": 106.8779},
    "Jakarta Timur": {"lat": -6.2250, "lon": 106.9004}
}

@task(retries=2, retry_delay_seconds=10)
def fetch_weather_and_pollution(region_name, coords):
    # Endpoint Cuaca
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={coords['lat']}&lon={coords['lon']}&appid={API_KEY}&units=metric"
    # Endpoint Polusi Udara
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={coords['lat']}&lon={coords['lon']}&appid={API_KEY}"
    
    weather_res = requests.get(weather_url).json()
    aqi_res = requests.get(aqi_url).json()
    
    return {
        "region": region_name,
        "data_timestamp": pd.to_datetime(weather_res["dt"], unit='s'),
        "temperature": weather_res["main"]["temp"],
        "feels_like": weather_res["main"]["feels_like"],
        "pressure": weather_res["main"]["pressure"],
        "humidity": weather_res["main"]["humidity"],
        "wind_speed": weather_res["wind"]["speed"],
        "weather_main": weather_res["weather"][0]["main"],
        "weather_desc": weather_res["weather"][0]["description"],
        "aqi": aqi_res["list"][0]["main"]["aqi"],
        "pm2_5": aqi_res["list"][0]["components"]["pm2_5"],
        "pm10": aqi_res["list"][0]["components"]["pm10"]
    }

@task
def process_and_save_parquet(data_list):
    df = pd.DataFrame(data_list)
    file_path = "data/processed/weather_analytics.parquet"
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    table = pa.Table.from_pandas(df)
    
    if os.path.exists(file_path):
        existing_table = pq.read_table(file_path)
        # Idempotency check: Hindari duplikasi timestamp untuk region yang sama
        existing_df = existing_table.to_pandas()
        merged_df = pd.concat([existing_df, df]).drop_duplicates(subset=['region', 'data_timestamp'], keep='last')
        final_table = pa.Table.from_pandas(merged_df)
        pq.write_table(final_table, file_path)
    else:
        pq.write_table(table, file_path)

@flow(name="Jakarta_Spatial_Weather_ETL")
def main_flow():
    all_data = []
    for region, coords in JAKARTA_REGIONS.items():
        data = fetch_weather_and_pollution(region, coords)
        all_data.append(data)
    
    process_and_save_parquet(all_data)

if __name__ == "__main__":
    main_flow()