import pandas as pd

from utils.filter_data_helper import filter_data
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
# df = pd.read_csv("./data/data.csv")
df = pd.read_csv("./data/fresh-data.csv")

df2 = filter_data(df)
df = df2

# Preprocessing data
X, y, preprocessor = preprocessing(df)

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

# # save model and preprocessor
# joblib.dump(model, "./models/model.pkl")
# joblib.dump(preprocessor, "./models/preprocessor.pkl")
# print("Modèle et préprocesseur enregistrés.")
