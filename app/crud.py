
from typing import List, Optional
from sqlalchemy.orm import Session
from models import ShortURL
from utils import generate_short_code


def create_short_url(db: Session, original_url: str, custom_code: Optional[str] = None) -> ShortURL:
    """
    Tworzy nowy skrócony URL w bazie danych.
    
    Args:
        db: Sesja bazy danych
        original_url: Oryginalny URL do skrócenia
        custom_code: Opcjonalny własny kod (jeśli None, generowany automatycznie)
    
    Returns:
        ShortURL: Utworzony obiekt skróconego URL
    
    Raises:
        ValueError: Gdy własny kod już istnieje w bazie
    """
    if custom_code:
        # Sprawdź, czy własny kod już istnieje
        existing = get_url_by_code(db, custom_code)
        if existing:
            raise ValueError(f"Kod '{custom_code}' już istnieje w bazie danych")
        short_code = custom_code
    else:
        # Pobierz wszystkie istniejące kody
        existing_codes = {url.short_code for url in get_all_urls(db)}
        short_code = generate_short_code(existing_codes=existing_codes)
    
    # Utwórz nowy obiekt
    db_url = ShortURL(
        original_url=original_url,
        short_code=short_code
    )
    
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    return db_url


def get_url_by_code(db: Session, short_code: str) -> Optional[ShortURL]:
    """
    Pobiera URL na podstawie krótkiego kodu.
    
    Args:
        db: Sesja bazy danych
        short_code: Krótki kod do wyszukania
    
    Returns:
        Optional[ShortURL]: Znaleziony obiekt lub None
    """
    return db.query(ShortURL).filter(ShortURL.short_code == short_code).first()


def get_all_urls(db: Session, limit: int = 100) -> List[ShortURL]:
    """
    Pobiera wszystkie skrócone URL z bazy danych.
    
    Args:
        db: Sesja bazy danych
        limit: Maksymalna liczba wyników (domyślnie 100)
    
    Returns:
        List[ShortURL]: Lista wszystkich skróconych URL
    """
    return db.query(ShortURL).order_by(ShortURL.created_at.desc()).limit(limit).all()


def delete_url(db: Session, short_code: str) -> bool:
    """
    Usuwa skrócony URL z bazy danych.
    
    Args:
        db: Sesja bazy danych
        short_code: Kod URL do usunięcia
    
    Returns:
        bool: True jeśli usunięto, False jeśli nie znaleziono
    """
    db_url = get_url_by_code(db, short_code)
    if db_url:
        db.delete(db_url)
        db.commit()
        return True
    return False


def increment_click_count(db: Session, short_code: str) -> bool:
    """
    Zwiększa licznik kliknięć dla danego URL.
    
    Args:
        db: Sesja bazy danych
        short_code: Kod URL
    
    Returns:
        bool: True jeśli zwiększono, False jeśli nie znaleziono
    """
    db_url = get_url_by_code(db, short_code)
    if db_url:
        db_url.click_count += 1
        db.commit()
        return True
    return False
