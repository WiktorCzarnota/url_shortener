
import streamlit as st
from sqlalchemy.orm import Session
from database import init_db, SessionLocal
from crud import (
    create_short_url,
    get_all_urls,
    delete_url,
    get_url_by_code,
    increment_click_count
)
from utils import validate_url


def initialize_app() -> None:
    """Inicjalizuje aplikację i bazę danych."""
    init_db()
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True


def get_database_session() -> Session:
    """
    Zwraca sesję bazy danych.
    
    Returns:
        Session: Sesja bazy danych SQLAlchemy
    """
    return SessionLocal()


def main() -> None:
    """Główna funkcja aplikacji Streamlit."""
    st.set_page_config(
        page_title="Skracacz URL",
        page_icon="🔗",
        layout="wide"
    )
    
    initialize_app()
    
    st.title("🔗 Skracacz URL")
    st.markdown("---")
    
    # Tworzenie dwóch kolumn dla lepszego layoutu
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Skróć nowy URL")
        
        # Formularz do skracania URL
        with st.form("url_form", clear_on_submit=True):
            original_url = st.text_input(
                "Wpisz URL do skrócenia:",
                placeholder="https://example.com/very/long/url/here"
            )
            
            custom_code = st.text_input(
                "Własny kod (opcjonalnie):",
                placeholder="mojkod",
                help="Jeśli pozostawisz puste, kod zostanie wygenerowany automatycznie"
            )
            
            submitted = st.form_submit_button("Skróć URL", type="primary")
            
            if submitted:
                if not validate_url(original_url):
                    st.error("❌ Nieprawidłowy URL! URL musi zaczynać się od http:// lub https://")
                else:
                    try:
                        db = get_database_session()
                        custom = custom_code.strip() if custom_code.strip() else None
                        
                        short_url_obj = create_short_url(db, original_url, custom)
                        
                        st.success(f"✅ URL został skrócony!")
                        st.code(f"Twój skrócony kod: {short_url_obj.short_code}")
                        st.info(f"💡 Oryginalny URL: {original_url}")
                        
                        db.close()
                    except ValueError as e:
                        st.error(f"❌ Błąd: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Wystąpił nieoczekiwany błąd: {str(e)}")
    
    with col2:
        st.header("Statystyki")
        db = get_database_session()
        all_urls = get_all_urls(db)
        
        st.metric("Liczba skróconych URL", len(all_urls))
        
        if all_urls:
            total_clicks = sum(url.click_count for url in all_urls)
            st.metric("Całkowita liczba kliknięć", total_clicks)
        
        db.close()
    
    # Sekcja z listą wszystkich URL
    st.markdown("---")
    st.header("📋 Lista skróconych URL")
    
    db = get_database_session()
    urls = get_all_urls(db)
    
    if not urls:
        st.info("Brak skróconych URL. Dodaj pierwszy!")
    else:
        # Wyszukiwanie
        search_term = st.text_input("🔍 Szukaj w URL:", placeholder="Wpisz część URL...")
        
        if search_term:
            urls = [url for url in urls if search_term.lower() in url.original_url.lower() 
                    or search_term.lower() in url.short_code.lower()]
        
        for url in urls:
            with st.expander(
                f"🔗 {url.short_code} → {url.original_url[:50]}..." if len(url.original_url) > 50 else f"🔗 {url.short_code} → {url.original_url}"
            ):
                col_a, col_b = st.columns([3, 1])
                
                with col_a:
                    st.write(f"**Skrócony kod:** `{url.short_code}`")
                    st.write(f"**Oryginalny URL:** {url.original_url}")
                    st.write(f"**Utworzono:** {url.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write(f"**Liczba kliknięć:** {url.click_count} 👆")
                
                with col_b:
                    if st.button("🗑️ Usuń", key=f"delete_{url.id}"):
                        if delete_url(db, url.short_code):
                            st.success("Usunięto!")
                            st.rerun()
                        else:
                            st.error("Błąd usuwania")
                    
                    if st.button("➕ Klik", key=f"click_{url.id}"):
                        if increment_click_count(db, url.short_code):
                            st.success("Zwiększono licznik!")
                            st.rerun()
    
    db.close()
    
    # Stopka
    st.markdown("---")
    st.markdown("Projekt wykonany w ramach kursu Podstawy Programowania w Pythonie")


if __name__ == "__main__":
    main()
