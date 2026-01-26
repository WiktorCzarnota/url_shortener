"""
Funkcje pomocnicze dla skracacza URL.
"""
import string
import random
from typing import Set


def generate_short_code(length: int = 6, existing_codes: Set[str] = None) -> str:
    """
    Generuje losowy krótki kod dla URL.
    
    Args:
        length: Długość generowanego kodu (domyślnie 6)
        existing_codes: Zbiór już istniejących kodów (opcjonalnie)
    
    Returns:
        str: Wygenerowany unikalny kod
    
    Raises:
        ValueError: Gdy nie można wygenerować unikalnego kodu po wielu próbach
    """
    if existing_codes is None:
        existing_codes = set()
    
    characters = string.ascii_letters + string.digits
    max_attempts = 100
    
    for _ in range(max_attempts):
        code = ''.join(random.choices(characters, k=length))
        if code not in existing_codes:
            return code
    
    raise ValueError("Nie można wygenerować unikalnego kodu po wielu próbach")


def validate_url(url: str) -> bool:
    """
    Sprawdza, czy URL jest poprawny (prosta walidacja).
    
    Args:
        url: URL do walidacji
    
    Returns:
        bool: True jeśli URL jest poprawny, False w przeciwnym razie
    """
    if not url or not isinstance(url, str):
        return False
    
    url = url.strip()
    
    # Prosta walidacja - URL musi zaczynać się od http:// lub https://
    return url.startswith(('http://', 'https://')) and len(url) > 10
