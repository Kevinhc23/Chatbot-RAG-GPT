FROM python:3-alpine

WORKDIR /app

# Actualizar pip antes de instalar dependencias
RUN pip install --no-cache-dir --upgrade pip

# Copiar el archivo requirements.txt desde el contexto de construcción
COPY requirements.txt /app/requirements.txt

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]