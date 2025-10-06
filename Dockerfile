# Dockerfile para Microservicio 5 - Orquestador
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Exponer puerto 8005
EXPOSE 8005

# Variables de entorno por defecto (pueden ser sobrescritas)
ENV MICROSERVICE1_URL=http://microservicio1:8081
ENV MICROSERVICE2_URL=http://microservicio2:3000
ENV MICROSERVICE3_URL=http://microservicio3:8000
ENV MICROSERVICE4_URL=http://microservicio4:8080

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
