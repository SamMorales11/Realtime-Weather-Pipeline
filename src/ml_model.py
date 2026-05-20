import pandas as pd
import duckdb
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score
import joblib
import os

def train_and_predict():
    # 1. Ekstraksi Data via DuckDB
    con = duckdb.connect()
    df = con.execute("SELECT * FROM 'data/processed/weather_analytics.parquet' ORDER BY data_timestamp ASC").df()
    
    if len(df) < 50:
        print("Data historis belum cukup untuk melatih model. Biarkan ingestion berjalan beberapa saat.")
        return

    # 2. Rekayasa Fitur (Feature Engineering)
    # Menggeser target suhu 1 langkah ke atas (memprediksi suhu berdasarkan cuaca 1 jam sebelumnya)
    df['target_temp_next_hour'] = df.groupby('region')['temperature'].shift(-1)
    df = df.dropna()

    features = ['humidity', 'pressure', 'wind_speed', 'aqi', 'pm2_5', 'pm10']
    X = df[features]
    y = df['target_temp_next_hour']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Inisialisasi & Pelatihan Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    rf_model.fit(X_train, y_train)

    # 4. Evaluasi Metrik
    predictions = rf_model.predict(X_test)
    rmse = root_mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"Model Evaluated - RMSE: {rmse:.4f} | R-squared: {r2:.4f}")

    # 5. Memprediksi Suhu Terbaru untuk Tiap Region
    latest_data = df.groupby('region').tail(1).copy()
    X_latest = latest_data[features]
    latest_predictions = rf_model.predict(X_latest)
    
    latest_data['predicted_temp'] = latest_predictions
    
    # 6. Menyimpan Hasil Prediksi ke Parquet Terpisah
    pred_path = "data/processed/weather_predictions.parquet"
    if os.path.exists(pred_path):
        existing_pred = pd.read_parquet(pred_path)
        combined = pd.concat([existing_pred, latest_data[['region', 'data_timestamp', 'predicted_temp']]])
        combined.to_parquet(pred_path)
    else:
        latest_data[['region', 'data_timestamp', 'predicted_temp']].to_parquet(pred_path)

if __name__ == "__main__":
    train_and_predict()