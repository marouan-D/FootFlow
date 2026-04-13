# FootFlow — Premier League Data Pipeline

FootFlow is een automatische data pipeline die Premier League voetbaldata ophaalt via de football-data.org API, opslaat in een MySQL database en visualiseert in een Streamlit dashboard.

## Technologie
- Python 3.11
- MySQL (XAMPP)
- Streamlit
- APScheduler
- pandas
- pytest

## Installatie

### 1. Repository clonen
```
git clone https://github.com/marouan-D/FootFlow.git
cd FootFlow
```

### 2. Packages installeren
```
pip install -r requirements.txt
```

### 3. .env bestand aanmaken
Maak een `.env` bestand aan in de `footflow` map:
```
API_KEY= hier_api_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=footflow
```

### 4. Database aanmaken
Start XAMPP en maak een database aan met de naam `footflow` via phpMyAdmin.

## Gebruik

### Pipeline starten
```
cd src
python main.py
```
Kies optie 1 om de pipeline direct te starten.

### Dashboard starten
```
cd src
streamlit run dashboard.py
```

### Testen uitvoeren
```
cd tests
pytest test_pipeline.py -v
```

## Project structuur
```
FootFlow/
├── src/
│   ├── main.py
│   ├── api.py
│   ├── database.py
│   ├── models.py
│   ├── collector.py
│   ├── transformer.py
│   ├── csv_handler.py
│   ├── dashboard.py
│   ├── scheduler.py
│   └── logger.py
├── data/
│   └── spelers.csv
├── tests/
│   └── test_pipeline.py
├── logs/
│   └── pipeline.log  (wordt automatisch aangemaakt bij eerste run)
├── .env
├── .gitignore
└── requirements.txt
```

## Gemaakt door
Marouan Didouch — Student Bit Academy Portfolio 2026
