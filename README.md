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

### Display API routes (Swagger)
```bash
[docs](http://127.0.0.1:8000/docs)
```

### Execute API test
```bash
pytest test_api.py
```

### Add database migration
```bash
alembic revision --autogenerate -m "mon nom de migration"
```

Apply migration
```bash
alembic upgrade head
```
