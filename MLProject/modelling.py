import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn

mlflow.set_experiment("Heart Disease CI Pipeline")

with mlflow.start_run():
    # 1. Load Data
    X_train = pd.read_csv("dataset_processed/X_train.csv")
    X_test = pd.read_csv("dataset_processed/X_test.csv")
    y_train = pd.read_csv("dataset_processed/y_train.csv").squeeze()
    y_test = pd.read_csv("dataset_processed/y_test.csv").squeeze()

    # 2. Train Model (Gunakan parameter standar saja untuk CI agar cepat)
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # 3. Prediksi dan Metrik
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", accuracy)

    # 4. Log Model (INI YANG PALING KRUSIAL AGAR DOCKER BISA BUILD)
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model"
    )

    print(f"Model CI berhasil dilatih dengan akurasi {accuracy:.4f} dan disimpan ke mlruns!")