# Python 3.12 (veya kullandığın versiyon) imajını kullan
FROM python:3.12-slim

# Çalışma dizinini ayarla
WORKDIR /code

# Bağımlılıkları kopyala ve yükle
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Tüm backend klasörünü kopyala
COPY . /code/

# FastAPI'yi çalıştır (Port 8000)
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]