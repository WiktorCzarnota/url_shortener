from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base

# Ścieżka do pliku bazy danych SQLite
DATABASE_URL = "sqlite:///./url_shortener.db"

# Tworzenie silnika bazy danych
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # Potrzebne dla SQLite
)

# SessionLocal to klasa do tworzenia sesji bazy danych
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """
    Inicjalizuje bazę danych, tworząc wszystkie tabele.
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """
    Generator zwracający sesję bazy danych.
    Zapewnia automatyczne zamknięcie sesji po użyciu.

    Yields:
        Session: Sesja bazy danych SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
