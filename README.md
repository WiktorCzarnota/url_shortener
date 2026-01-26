# Skracacz URL - Projekt w Streamlit

Prosty skracacz adresów URL stworzony w ramach kursu "Podstawy programowania w Pythonie".

## Opis projektu

Aplikacja webowa umożliwiająca skracanie długich adresów URL do krótkich, łatwych do zapamiętania kodów. Aplikacja przechowuje dane w bazie SQLite i pozwala na:
- Tworzenie skróconych URL (z automatycznym lub własnym kodem)
- Przeglądanie wszystkich skróconych URL
- Usuwanie skróconych URL
- Śledzenie liczby kliknięć w każdy link
- Wyszukiwanie w bazie URL

## Technologie

- **Python 3.11+**
- **Streamlit** - framework do tworzenia aplikacji webowych
- **SQLAlchemy** - ORM do pracy z bazą danych
- **SQLite** - baza danych
- **pytest** - framework do testów jednostkowych

## Struktura projektu

```
url_shortener/
├── app/
│   ├── __init__.py
│   ├── main.py          # Główna aplikacja Streamlit
│   ├── models.py        # Modele SQLAlchemy
│   ├── database.py      # Konfiguracja bazy danych
│   ├── crud.py          # Operacje CRUD
│   └── utils.py         # Funkcje pomocnicze
├── tests/
│   ├── __init__.py
│   ├── test_crud.py     # Testy operacji CRUD
│   └── test_utils.py    # Testy funkcji pomocniczych
├── requirements.txt     # Zależności projektu
├── README.md           # Ten plik
├── raport.md           # Raport z diagramem ERD
├── Dockerfile          # Konfiguracja Docker
└── docker-compose.yml  # Docker Compose
```

## Instalacja i uruchomienie

### Sposób 1: Standardowa instalacja

### Sposób 1: Standardowa instalacja

1. Sklonuj repozytorium:
```bash
git clone <https://github.com/WiktorCzarnota/url_shortener.git>
cd url_shortener
```

2. Utwórz środowisko wirtualne (zalecane, można ominąć):
```bash
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
# lub
venv\Scripts\activate.bat     # Windows CMD
# lub
source venv/bin/activate      # Linux/Mac
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Uruchom aplikację:
```bash
streamlit run app/main.py
```

5. Otwórz przeglądarkę pod adresem: `http://localhost:8501`

### Sposób 2: Docker (zalecany)

1. Zbuduj i uruchom kontener:
```bash
docker-compose up --build
```

2. Otwórz przeglądarkę pod adresem: `http://localhost:8501`

3. Zatrzymanie:
```bash
docker-compose down
```

## Uruchamianie testów

```bash
pytest tests/ -v
```

Test na dym (podstawowy test całej aplikacji):
```bash
pytest tests/test_crud.py::test_smoke_test -v
```

## Funkcjonalności

### Skracanie URL
1. Wpisz długi URL (musi zaczynać się od `http://` lub `https://`)
2. Opcjonalnie: podaj własny kod
3. Kliknij "Skróć URL"
4. Otrzymasz unikalny 6-znakowy kod (lub własny, jeśli podałeś)

### Zarządzanie URL
- **Lista wszystkich URL**: Wyświetla wszystkie skrócone linki z datą utworzenia i liczbą kliknięć
- **Wyszukiwanie**: Filtruj URL po kodzie lub oryginalnym adresie
- **Usuwanie**: Usuń niepotrzebne skrócone URL
- **Licznik kliknięć**: Symuluj kliknięcia w linki

## Baza danych

Aplikacja używa SQLite z następującym schematem:

**Tabela: short_urls**
- `id` (INTEGER, PRIMARY KEY)
- `original_url` (STRING, NOT NULL)
- `short_code` (STRING, UNIQUE, NOT NULL)
- `created_at` (DATETIME)
- `click_count` (INTEGER, DEFAULT 0)

Szczegółowy diagram ERD znajduje się w pliku `raport.md`.

## Zgodność z PEP8

Kod jest zgodny z PEP8. Sprawdzenie:
```bash
pip install flake8
flake8 app/ tests/ --max-line-length=100
```

## Autor

Wiktor Czarnota

## Licencja

Projekt edukacyjny - brak licencji komercyjnej.
