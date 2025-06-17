# Description
The aim of this project is create a model from witch with data added into a database by using SQLAlchemy.


## Virtual environment

Linux :
```bash
python3 -m venv .venv
```

MacOS-Windows
```bash
python -m venv .venv
```

## Activate Virtual environment :
Windows : 
```bash
.venv\Scripts\activate
```

macOS/Linux : 
```bash
source .venv/bin/activate
```

## Dependencies :

* Make sure you're in the project directory
* Install dependencies : `pip install -r requirements.txt`
* Alternatively, you can install the libraries yourself by reading requierements.txt file
  
### Project structure
```bash
.
├── crud
│   └── client.py
├── data
│   └── data.csv
├── database.py
├── main.py
├── models
│   └── client.py
├── notebook.ipynb
├── README.md
├── requirements.txt
├── routes
│   └── client.py
├── run.py
└── schemas
    └── client.py

```

### Launch project
```bash
python3 run.py
```

### Execute API test
```bash
pytest pytest test_api.py
```

### Add database migration
```bash
alembic revision --autogenerate -m "mon nom de migration"
```

Apply migration
```bash
alembic upgrade head
```



Qu’est-ce que j’ai fait ?
- Mise en place d'un notebook pour comprendre le fonctionnement de la lib sqlalchemy
- Création d'une BDD à partir d'un fichier CSV en python
- Mise en place d'une API avec plusieurs route pour requeter ma bdd*
- Ajout de plusieurs tests avec pytest afin de valider le bon fonctionnement de mes routes
- Implémentation d'alembic pour gérer les migrations de la bdd
- Mise en place de l'entrainement d'un model à partir d'un jeu de données


Quelles difficultés j’ai rencontrées dans la journée ?
- Petit souci sur le typage des retours dans mes apis entre sqlalchemy et pydantic
  
Qu’est-ce que j’ai appris ?
- À utiliser sqlalchemy & alembic
- La différence entre une colonne categorielle set manuellement 0,1,2,3 et avec dummies (colonne à plat sans hiérarchie)
- La "cuisine" possible à réaliser sur la densité des neuronnes
