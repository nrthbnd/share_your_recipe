cd foodgram_backend || exit
python manage.py migrate;
python manage.py collectstatic --noinput;
gunicorn -b 0:8000 foodgram.wsgi;