import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential


def preprocessing(df, numerical_cols, categorical_cols, predict_col):
    num_pipeline = Pipeline(
        [("imputer", SimpleImputer(strategy="mean")), ("scaler", StandardScaler())]
    )

    cat_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        [("num", num_pipeline, numerical_cols), ("cat", cat_pipeline, categorical_cols)]
    )

    y = predict_col

    X_processed = preprocessor.fit_transform(df)

    return X_processed, y, preprocessor


def train_model(
    model, X, y, X_val=None, y_val=None, epochs=50, batch_size=32, verbose=0
):
    hist = model.fit(
        X,
        y,
        validation_data=(X_val, y_val)
        if X_val is not None and y_val is not None
        else None,
        epochs=epochs,
        batch_size=batch_size,
        verbose=verbose,
    )
    return model, hist


def evaluate_performance(y_true, y_pred):
    """
    Fonction pour mesurer les performances du modèle avec MSE, MAE et R².
    """
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {"MSE": mse, "MAE": mae, "R²": r2}


def model_predict(model, X):
    y_pred = model.predict(X).flatten()
    return y_pred


def print_data(dico, exp_name):
    mse = dico["MSE"]
    mae = dico["MAE"]
    r2 = dico["R²"]

    print(f"{exp_name:^60}".replace(" ", "="))
    print(f"MSE: {mse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}")
    print("=" * 60)


def draw_loss(history):
    """
    Affiche les courbes de loss et val_loss de l'historique d'entraînement.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(history.history["loss"], label="Loss (Entraînement)")
    plt.plot(history.history["val_loss"], label="Val Loss (Validation)", linestyle="--")
    plt.title("Courbes de Loss et Val Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)
    plt.show()


def draw_loss_mlflow(history, mlflow):
    """
    Display loss and val_loss in mlflow.
    """

    plt.figure(figsize=(10, 5))
    plt.plot(history.history["loss"], label="Train Loss")
    if "val_loss" in history.history:
        plt.plot(history.history["val_loss"], label="Validation Loss")
    plt.title("Courbe de perte")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()

    mlflow.log_figure(plt.gcf(), "loss_curve.png")
    plt.close()


def split(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


def create_nn_model(input_dim):
    """
    Fonction pour créer et compiler un modèle de réseau de neurones simple.
    """
    model = Sequential()
    model.add(Dense(12, activation="relu", input_dim=input_dim))
    model.add(Dense(6, activation="relu"))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")
    return model
