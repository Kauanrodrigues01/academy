# Use uma imagem base do Python
FROM python:3.9-slim

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho
COPY . /app/

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Instalar dependências do Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expor a porta para o servidor
EXPOSE 8000

# Comando para rodar a aplicação com Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn project.wsgi:application --bind 0.0.0.0:8000 & celery -A project worker --loglevel=info & celery -A project beat --loglevel=info"]
