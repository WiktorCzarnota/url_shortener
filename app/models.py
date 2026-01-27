from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ShortURL(Base):
    """Model reprezentujący skrócony URL w bazie danych.

    Attributes:
        id (int): Unikalny identyfikator
        original_url (str): Oryginalny, długi URL
        short_code (str): Krótki kod identyfikujący URL
        created_at (datetime): Data utworzenia skrótu
        click_count (int): Liczba kliknięć w skrócony link
    """

    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now)
    click_count = Column(Integer, default=0)

    def __repr__(self) -> str:
        """Reprezentacja tekstowa obiektu."""
        return f"<ShortURL(short_code='{self.short_code}', clicks={self.click_count})>"
