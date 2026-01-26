# Używamy oficjalnego obrazu Python
FROM python:3.11-slim

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy pliki requirements
COPY requirements.txt .

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy cały projekt
COPY . .

# Otwieramy port dla Streamlit
EXPOSE 8501

# Uruchamiamy aplikację
CMD ["streamlit", "run", "app/main.py", "--server.address", "0.0.0.0"]
