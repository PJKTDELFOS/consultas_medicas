#!/bin/bash

set -e
echo "1. Coletando arquivos estáticos (CSS, JS, Imagens)..."
python manage.py collectstatic --noinput

echo "2. Aplicando migrações no Banco de Dados..."
python manage.py migrate --noinput

echo "3. Criando admin do sistema"
DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD python manage.py createsuperuser --noinput --username adminalbert --email albert.franca1992@gmail.com || true

echo "4. Iniciando o servidor Gunicorn (Produção)..."
# ATENÇÃO: Substitua 'appa_project' pelo nome exato da pasta onde está o seu arquivo wsgi.py!
if [ "$DEBUG" = "True" ]; then
    echo "4. Iniciando o servidor de Desenvolvimento (Django Runserver)..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "4. Iniciando o servidor de Produção (Gunicorn)..."
    # AJUSTADO: Agora aponta corretamente para testelacrei.wsgi!
    exec gunicorn testelacrei.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi