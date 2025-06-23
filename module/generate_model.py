import os

import mlflow
import mlflow.artifacts
import mlflow.tensorflow
import pandas as pd
import tensorflow as tf

from utils import (
    create_nn_model,
    draw_loss,
    evaluate_performance,
    model_predict,
    preprocessing,
    print_data,
    split,
    train_model,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def simple_model_train(csv_name, numerical_cols, categorical_cols, predict_col):
    # Load data
    data_path = os.path.join(BASE_DIR, "data", csv_name)
    df = pd.read_csv(data_path)

    # Set column to predict
    predict = df[predict_col]

    # Preprocessing data
    X, y, _ = preprocessing(df, numerical_cols, categorical_cols, predict)

    # split data in train and test dataset
    X_train, X_test, y_train, y_test = split(X, y)

    # create a new model
    model = create_nn_model(X_train.shape[1])

    # First model train
    model, hist = train_model(model, X_train, y_train, X_val=X_test, y_val=y_test)
    y_pred = model_predict(model, X_test)
    perf = evaluate_performance(y_test, y_pred)
    print_data(perf, "Performance after training")

    # display val loss graph
    draw_loss(hist)

    # Save model
    model.save(os.path.join(BASE_DIR, "model_artifacts", "model1.keras"))
    print("Model and preprocessor saved.")

    # Log dans MLflow
    mlflow.set_experiment("SQL-ALCHEMY-MODEL-TRAIN")
    with mlflow.start_run(run_name="Train Keras Model"):
        mlflow.log_metric("mse", perf["MSE"])
        mlflow.log_metric("mae", perf["MAE"])
        mlflow.log_metric("r2", perf["R²"])
        # mlflow.artifacts
        mlflow.tensorflow.log_model(model, artifact_path="model")


def train_model_from_existing(
    model_name, csv_name, numerical_cols, categorical_cols, predict_col
):
    # Load given model name
    model_path = os.path.join(BASE_DIR, "model_artifacts", model_name)
    model1_loaded = tf.keras.models.load_model(model_path)

    # Load data
    data_path = os.path.join(BASE_DIR, "data", csv_name)
    df = pd.read_csv(data_path)

    # Set column to predict
    predict = df[predict_col]

    # Preprocessing data
    X, y, _ = preprocessing(df, numerical_cols, categorical_cols, predict)

    # split data in train and test dataset
    X_train, X_test, y_train, y_test = split(X, y)

    # create a new model
    model2 = create_nn_model(X_train.shape[1])

    # Transfer layer weight
    for layer in model2.layers:
        try:
            old_layer = model1_loaded.get_layer(name=layer.name)
            layer.set_weights(old_layer.get_weights())
            print(f"✅ Poids transférés pour : {layer.name}")
        except (ValueError, KeyError):
            print(f"⛔ Incompatible ou nouvelle couche : {layer.name}")

    # Train model with new data
    new_model, hist = train_model(model2, X_train, y_train, X_val=X_test, y_val=y_test)
    y_pred = model_predict(new_model, X_test)
    perf = evaluate_performance(y_test, y_pred)
    print_data(perf, "Performance after training")

    # display val loss graph
    draw_loss(hist)

    # Save model
    new_model.save(os.path.join(BASE_DIR, "model_artifacts", "model2.keras"))
    print("Model and preprocessor saved.")

    mlflow.set_experiment("SQL-ALCHEMY-MODEL-TRAIN")
    with mlflow.start_run(run_name="Retrained Keras Model"):
        mlflow.log_metric("mse", perf["MSE"])
        mlflow.log_metric("mae", perf["MAE"])
        mlflow.log_metric("r2", perf["R²"])
        mlflow.tensorflow.log_model(new_model, artifact_path="model")
