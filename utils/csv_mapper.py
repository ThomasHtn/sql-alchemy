# Mapping between CSV property and SQLAlchemy model
CSV_TO_DB_MAP = {
    "age": "age",
    "taille": "height_cm",
    "poids": "weight_kg",
    "sport_licence": "has_sports_license",
    "niveau_etude": "education_level",
    "region": "region",
    "smoker": "is_smoker",
    "revenu_estime_mois": "estimated_monthly_income",
    "situation_familiale": "marital_status",
    "historique_credits": "credit_history",
    "risque_personnel": "personal_risk_score",
    "score_credit": "credit_score",
    "loyer_mensuel": "monthly_rent",
    "montant_pret": "loan_amount_requested",
    "nb_enfants": "nb_enfants",
    "quotient_caf": "quotient_caf",
}

# Boolean mapper
BOOL_MAP = {"oui": True, "non": False, "": None}

# Education mapper
EDUCATION_MAP = {
    "aucun": 0,
    "primaire": 1,
    "college": 2,
    "lycée": 3,
    "bac": 4,
    "bac+2": 5,
    "bac+3": 6,
    "master": 7,
    "doctorat": 8,
}

SITUATION_FAMILIALE_MAP = {
    "célibataire": 0,
    "séparé": 1,
    "divorcé": 2,
    "veuf": 3,
    "concubinage": 4,
    "pacsé": 5,
    "marié": 6,
}
