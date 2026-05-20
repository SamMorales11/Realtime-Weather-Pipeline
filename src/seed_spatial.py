import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
from datetime import datetime, timedelta
import os

JAKARTA_REGIONS = ["Jakarta Pusat", "Jakarta Selatan", "Jakarta Barat", "Jakarta Utara", "Jakarta Timur"]

data = []
now = datetime.now()

# Menghasilkan data historis tiruan untuk 24 jam terakhir di 5 wilayah
for region in JAKARTA_REGIONS:
    for i in range(24, 0, -1):
        timestamp = now - timedelta(hours=i)
        data.append({
            "region": region,
            "data_timestamp": timestamp,
            "temperature": round(np.random.uniform(26.0, 35.0), 2),
            "feels_like": round(np.random.uniform(28.0, 38.0), 2),
            "pressure": np.random.randint(1005, 1015),
            "humidity": np.random.randint(55, 90),
            "wind_speed": round(np.random.uniform(1.0, 6.0), 2),
            "weather_main": "Clouds",
            "weather_desc": "scattered clouds",
            "aqi": np.random.randint(1, 5),
            "pm2_5": round(np.random.uniform(15.0, 65.0), 2),
            "pm10": round(np.random.uniform(25.0, 85.0), 2)
        })

df = pd.DataFrame(data)
file_path = "data/processed/weather_analytics.parquet"

os.makedirs(os.path.dirname(file_path), exist_ok=True)
table = pa.Table.from_pandas(df)
pq.write_table(table, file_path)

print("✅ Berhasil menyuntikkan 120 baris matriks fitur historis spasial!")