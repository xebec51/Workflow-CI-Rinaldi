import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import sklearn

# Dilarang menggunakan mlflow.set_experiment() di sini

with mlflow.start_run():
    # 1. Load Data
    X_train = pd.read_csv("dataset_processed/X_train.csv")
    X_test = pd.read_csv("dataset_processed/X_test.csv")
    y_train = pd.read_csv("dataset_processed/y_train.csv").squeeze()
    y_test = pd.read_csv("dataset_processed/y_test.csv").squeeze()

    # 2. Train Model
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # 3. Prediksi dan Metrik
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", accuracy)

    # 4. MEMAKSA LINGKUNGAN PYTHON 3.12.7 SECARA HARDCODE (SOLUSI DOCKER BUILD ERROR)
    custom_env = {
        "channels": ["conda-forge"],
        "dependencies": [
            "python=3.12.7",  # Kunci utamanya ada di sini!
            "pip",
            {
                "pip": [
                    "mlflow==2.19.0",
                    f"scikit-learn=={sklearn.__version__}",
                    "pandas"
                ]
            },
        ],
        "name": "mlflow-env"
    }

    # 5. Log Model dengan menyuntikkan Custom Environment
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        conda_env=custom_env
    )

    print(f"Model CI berhasil dilatih dengan akurasi {accuracy:.4f} dan Environment Python 3.12.7 terkunci!")