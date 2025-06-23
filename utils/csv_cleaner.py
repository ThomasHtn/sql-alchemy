import os
from os.path import join as join

import pandas as pd

from utils.outliers import outliers_filter

# GET base DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# =====================================
# Function to clean CSV and save result
#
# Inputs exemple :
#     columns_to_remove=["nom", "prenom", "sexe", "orientation_sexuelle"],
#     columns_to_categorised={"niveau_etude": EDUCATION_MAP},
#     columns_fillna_mean=["quotient_caf", "revenu_estime_mois"],
#     columns_fillna_mode=["situation_familiale"],
#     columns_outliers_filter=["revenu_estime_mois", "loyer_mensuel"]
# =====================================
def clean_and_save_csv(
    path,
    columns_to_remove: list[str],
    columns_to_categorised: dict[str, dict],
    columns_fillna_mean: list[str],
    columns_fillna_mode: list[str],
    columns_outliers_filter: list[str],
):
    # Load data
    data_path = os.path.join(BASE_DIR, "data", path)
    df = pd.read_csv(data_path)

    # Read csv
    df = pd.read_csv(data_path)

    # Remove undesirable columns if exist
    df = df.drop(columns=[col for col in columns_to_remove if col in df.columns])

    # Transformation of category columns
    for col, mapping in columns_to_categorised.items():
        if col in df.columns:
            df[col] = df[col].str.strip().str.lower().map(mapping)

    # Replace NaN by mean
    for col in columns_fillna_mean:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            mean_value = df[col].mean()
            df[col].fillna(mean_value, inplace=True)

    # Replace NaN by most frequent (mode)
    for col in columns_fillna_mode:
        if col in df.columns:
            mode_series = df[col].mode()
            if not mode_series.empty:
                mode_val = mode_series[0]
                df[col].fillna(mode_val, inplace=True)

    # Remove outliers
    for col in columns_outliers_filter:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            df = outliers_filter(df, col)

    # Save cleaned CSV
    df.to_csv(os.path.join(BASE_DIR, "data", "clean-data.csv"), index=False)

    print("CSV cleaned and saved in data directory")
