from utils.outliers import outliers_filter

def filter_data(df):
    df2 = outliers_filter(df, "revenu_estime_mois")
    df2 = outliers_filter(df, "age")
    df2 = outliers_filter(df, "risque_personnel")
    df2 = outliers_filter(df, "loyer_mensuel")
    df2 = outliers_filter(df, "montant_pret")
    df = df2

    return df