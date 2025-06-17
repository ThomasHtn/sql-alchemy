import pandas as pd

from utils.trainer_helper import (
    create_nn_model,
    draw_loss,
    evaluate_performance,
    model_predict,
    preprocessing,
    print_data,
    split,
    train_model,
)

# Load data
df = pd.read_csv("./data/data.csv")

# Preprocessing data
X, y, preprocessor = preprocessing(df)

# split data in train and test dataset
X_train, X_test, y_train, y_test = split(X, y)

# create a new model
model = create_nn_model(X_train.shape[1])

# monitoring default train value performances MSE, MAE et R²
y_pred = model_predict(model, X_train)
perf = evaluate_performance(y_train, y_pred)
print_data(perf, "Default train performance")

# monitoring default test value performances MSE, MAE et R²
y_pred = model_predict(model, X_test)
perf = evaluate_performance(y_test, y_pred)
print_data(perf, "Default test performance")


# First model train
model, hist = train_model(model, X_train, y_train, X_val=X_test, y_val=y_test)
y_pred = model_predict(model, X_test)
perf = evaluate_performance(y_test, y_pred)
print_data(perf, "Performance after training")

# display val loss graph
draw_loss(hist)

# # Display result in MLFLOW
# mlflow.set_experiment("EXPERIMENT_NAME")
# with mlflow.start_run(run_name="Default"):
#     # Log metrics in MLflow
#     mlflow.log_metric("mse", perf["MSE"])
#     mlflow.log_metric("mae", perf["MAE"])
#     mlflow.log_metric("r2", perf["R²"])

#     # Model
#     mlflow.sklearn.log_model(model, artifact_path="model")


# # save model and preprocessor
# joblib.dump(model, "./models/model.pkl")
# joblib.dump(preprocessor, "./models/preprocessor.pkl")
# print("Modèle et préprocesseur enregistrés.")
