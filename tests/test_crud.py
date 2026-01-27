import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import sys
from pathlib import Path

# Dodaj folder app do ścieżki
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from models import Base, ShortURL
from crud import (
    create_short_url,
    get_url_by_code,
    get_all_urls,
    delete_url,
    increment_click_count,
)


@pytest.fixture
def test_db() -> Session:
    """Fixture tworzący tymczasową bazę danych w pamięci dla testów.

    Yields:
        Session: Sesja testowej bazy danych
    """
    # Tworzenie silnika bazy danych w pamięci
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()

    yield db

    db.close()


class TestCreateShortUrl:
    """Testy dla funkcji create_short_url."""

    def test_create_with_auto_code(self, test_db: Session) -> None:
        """Test tworzenia URL z automatycznie generowanym kodem."""
        url = create_short_url(test_db, "https://example.com")

        assert url.original_url == "https://example.com"
        assert len(url.short_code) == 6
        assert url.click_count == 0

    def test_create_with_custom_code(self, test_db: Session) -> None:
        """Test tworzenia URL z własnym kodem."""
        url = create_short_url(test_db, "https://example.com", "custom")

        assert url.short_code == "custom"
        assert url.original_url == "https://example.com"

    def test_duplicate_custom_code_raises_error(self, test_db: Session) -> None:
        """Test, że duplikat własnego kodu rzuca wyjątek."""
        create_short_url(test_db, "https://example.com", "duplicate")

        with pytest.raises(ValueError):
            create_short_url(test_db, "https://another.com", "duplicate")


class TestGetUrlByCode:
    """Testy dla funkcji get_url_by_code."""

    def test_get_existing_url(self, test_db: Session) -> None:
        """Test pobierania istniejącego URL."""
        created = create_short_url(test_db, "https://example.com", "testcode")

        retrieved = get_url_by_code(test_db, "testcode")

        assert retrieved is not None
        assert retrieved.short_code == "testcode"
        assert retrieved.original_url == "https://example.com"

    def test_get_nonexistent_url(self, test_db: Session) -> None:
        """Test pobierania nieistniejącego URL."""
        result = get_url_by_code(test_db, "nonexistent")
        assert result is None


class TestGetAllUrls:
    """Testy dla funkcji get_all_urls."""

    def test_get_all_empty(self, test_db: Session) -> None:
        """Test pobierania z pustej bazy."""
        urls = get_all_urls(test_db)
        assert len(urls) == 0

    def test_get_all_multiple(self, test_db: Session) -> None:
        """Test pobierania wielu URL."""
        create_short_url(test_db, "https://example1.com", "code1")
        create_short_url(test_db, "https://example2.com", "code2")
        create_short_url(test_db, "https://example3.com", "code3")

        urls = get_all_urls(test_db)
        assert len(urls) == 3

    def test_get_all_respects_limit(self, test_db: Session) -> None:
        """Test, że limit działa poprawnie."""
        for i in range(10):
            create_short_url(test_db, f"https://example{i}.com")

        urls = get_all_urls(test_db, limit=5)
        assert len(urls) == 5


class TestDeleteUrl:
    """Testy dla funkcji delete_url."""

    def test_delete_existing_url(self, test_db: Session) -> None:
        """Test usuwania istniejącego URL."""
        create_short_url(test_db, "https://example.com", "todelete")

        result = delete_url(test_db, "todelete")
        assert result is True

        # Sprawdź, czy rzeczywiście usunięto
        retrieved = get_url_by_code(test_db, "todelete")
        assert retrieved is None

    def test_delete_nonexistent_url(self, test_db: Session) -> None:
        """Test usuwania nieistniejącego URL."""
        result = delete_url(test_db, "nonexistent")
        assert result is False


class TestIncrementClickCount:
    """Testy dla funkcji increment_click_count."""

    def test_increment_existing_url(self, test_db: Session) -> None:
        """Test zwiększania licznika dla istniejącego URL."""
        create_short_url(test_db, "https://example.com", "clicks")

        result = increment_click_count(test_db, "clicks")
        assert result is True

        url = get_url_by_code(test_db, "clicks")
        assert url.click_count == 1

    def test_increment_multiple_times(self, test_db: Session) -> None:
        """Test wielokrotnego zwiększania licznika."""
        create_short_url(test_db, "https://example.com", "multiclick")

        for _ in range(5):
            increment_click_count(test_db, "multiclick")

        url = get_url_by_code(test_db, "multiclick")
        assert url.click_count == 5

    def test_increment_nonexistent_url(self, test_db: Session) -> None:
        """Test zwiększania licznika dla nieistniejącego URL."""
        result = increment_click_count(test_db, "nonexistent")
        assert result is False


def test_smoke_test(test_db: Session) -> None:
    """Test na dym - sprawdza podstawowy przepływ działania aplikacji.
    """
    # Tworzenie URL
    url1 = create_short_url(test_db, "https://example.com")
    assert url1 is not None

    # Pobieranie URL
    retrieved = get_url_by_code(test_db, url1.short_code)
    assert retrieved is not None

    # Zwiększanie licznika
    increment_click_count(test_db, url1.short_code)
    updated = get_url_by_code(test_db, url1.short_code)
    assert updated.click_count == 1

    # Pobieranie wszystkich
    all_urls = get_all_urls(test_db)
    assert len(all_urls) >= 1

    # Usuwanie
    delete_url(test_db, url1.short_code)
    deleted = get_url_by_code(test_db, url1.short_code)
    assert deleted is None
