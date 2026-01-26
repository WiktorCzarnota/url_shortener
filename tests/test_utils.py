import pytest
import sys
from pathlib import Path

# Dodaj folder app do ścieżki
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from utils import generate_short_code, validate_url


class TestGenerateShortCode:
    """Testy dla funkcji generate_short_code."""

    def test_default_length(self) -> None:
        """Test domyślnej długości kodu."""
        code = generate_short_code()
        assert len(code) == 6

    def test_custom_length(self) -> None:
        """Test własnej długości kodu."""
        code = generate_short_code(length=10)
        assert len(code) == 10

    def test_uniqueness(self) -> None:
        """Test unikalności generowanych kodów."""
        codes = {generate_short_code() for _ in range(100)}
        # Powinniśmy otrzymać 100 unikalnych kodów
        assert len(codes) == 100

    def test_excludes_existing_codes(self) -> None:
        """Test wykluczania istniejących kodów."""
        existing = {"abc123", "def456", "ghi789"}
        for _ in range(50):
            code = generate_short_code(existing_codes=existing)
            assert code not in existing

    def test_contains_valid_characters(self) -> None:
        """Test, czy kod zawiera tylko dozwolone znaki."""
        import string

        valid_chars = set(string.ascii_letters + string.digits)

        code = generate_short_code()
        assert all(c in valid_chars for c in code)


class TestValidateUrl:
    """Testy dla funkcji validate_url."""

    def test_valid_http_url(self) -> None:
        """Test poprawnego URL z http."""
        assert validate_url("http://example.com") is True

    def test_valid_https_url(self) -> None:
        """Test poprawnego URL z https."""
        assert validate_url("https://example.com") is True

    def test_invalid_no_protocol(self) -> None:
        """Test niepoprawnego URL bez protokołu."""
        assert validate_url("example.com") is False

    def test_invalid_empty_string(self) -> None:
        """Test pustego stringa."""
        assert validate_url("") is False

    def test_invalid_none(self) -> None:
        """Test wartości None."""
        assert validate_url(None) is False

    def test_invalid_too_short(self) -> None:
        """Test zbyt krótkiego URL."""
        assert validate_url("http://a") is False

    def test_url_with_path(self) -> None:
        """Test URL ze ścieżką."""
        assert validate_url("https://example.com/path/to/resource") is True

    def test_url_with_query(self) -> None:
        """Test URL z parametrami zapytania."""
        assert validate_url("https://example.com/search?q=python") is True
