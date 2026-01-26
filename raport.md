# Raport projektu: Skracacz URL

## Opis projektu

Skracacz URL to aplikacja webowa stworzona w technologii Streamlit, która umożliwia użytkownikom skracanie długich adresów URL do krótkich, łatwych do zapamiętania kodów. Aplikacja przechowuje wszystkie dane w bazie SQLite i oferuje pełne zarządzanie skróconymi linkami.

## Główne funkcjonalności

1. **Skracanie URL**
   - Automatyczne generowanie 6-znakowego kodu
   - Możliwość podania własnego kodu
   - Walidacja poprawności URL (wymagany protokół http/https)

2. **Przeglądanie i zarządzanie**
   - Lista wszystkich skróconych URL
   - Wyświetlanie daty utworzenia
   - Licznik kliknięć dla każdego linku
   - Wyszukiwanie po kodzie lub oryginalnym URL

3. **Operacje**
   - Dodawanie nowych skróconych URL
   - Usuwanie istniejących URL
   - Symulacja kliknięć (inkrementacja licznika)

4. **Statystyki**
   - Całkowita liczba skróconych URL
   - Suma wszystkich kliknięć

## Diagram ERD (Entity-Relationship Diagram)

```
┌─────────────────────────────────────┐
│          short_urls                 │
├─────────────────────────────────────┤
│ id              INTEGER (PK)        │
│ original_url    VARCHAR NOT NULL    │
│ short_code      VARCHAR UNIQUE      │
│ created_at      DATETIME            │
│ click_count     INTEGER DEFAULT 0   │
└─────────────────────────────────────┘

Legenda:
- PK = Primary Key (klucz główny)
- UNIQUE = wartość musi być unikalna
- NOT NULL = pole wymagane
- DEFAULT = wartość domyślna
```

### Opis kolumn tabeli `short_urls`:

- **id**: Unikalny identyfikator każdego rekordu (klucz główny, auto-increment)
- **original_url**: Pełny, oryginalny adres URL, który użytkownik chce skrócić
- **short_code**: Krótki, unikalny kod identyfikujący skrócony URL (np. "abc123")
- **created_at**: Data i czas utworzenia skróconego URL
- **click_count**: Licznik kliknięć/użyć danego skróconego linku

### Indeksy:

- Indeks na `id` (primary key, automatyczny)
- Indeks na `short_code` (dla szybkiego wyszukiwania po kodzie)

## Technologie użyte w projekcie

- **Backend**: Python 3.11+ z SQLAlchemy ORM
- **Frontend**: Streamlit
- **Baza danych**: SQLite3
- **Testy**: pytest
- **Konteneryzacja**: Docker + Docker Compose

## Architektura aplikacji

Aplikacja została zaprojektowana zgodnie z zasadą separation of concerns:

1. **models.py** - definicje modeli danych (SQLAlchemy)
2. **database.py** - konfiguracja połączenia z bazą danych
3. **crud.py** - operacje CRUD (Create, Read, Update, Delete)
4. **utils.py** - funkcje pomocnicze (generowanie kodów, walidacja)
5. **main.py** - interfejs użytkownika Streamlit

## Przepływ danych

1. Użytkownik wprowadza URL przez interfejs Streamlit
2. URL jest walidowany (utils.py)
3. Generowany jest unikalny kod (utils.py)
4. Dane są zapisywane do bazy przez ORM (crud.py)
5. Interfejs wyświetla potwierdzenie i listę URL

## Bezpieczeństwo i dobre praktyki

- Walidacja wszystkich danych wejściowych
- Używanie ORM zamiast surowych zapytań SQL (ochrona przed SQL injection)
- Obsługa wyjątków na każdym poziomie
- Testy jednostkowe pokrywające główne funkcjonalności
- Typowanie wszystkich funkcji
- Dokumentacja w docstringach
- Zgodność z PEP8

## Możliwe rozszerzenia

- Dodanie autentykacji użytkowników
- Statystyki zaawansowane (geolokalizacja, przeglądarka, czas kliknięć)
- Opcja wygasania linków po określonym czasie
- API REST do programistycznego dostępu
- Własna domena do skróconych linków
- QR kody dla skróconych URL

## Podsumowanie

Projekt spełnia wszystkie wymagania określone w wytycznych:
- ✅ Baza danych z ORM (SQLAlchemy)
- ✅ Możliwość dodawania i usuwania danych
- ✅ Diagram ERD
- ✅ Docker Compose
- ✅ Testy jednostkowe
- ✅ PEP8, docstringi, typowanie
- ✅ README.md i requirements.txt
