FROM python:3.9-slim

WORKDIR /app

COPY backend/foodgram_backend/requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY backend/foodgram_backend/ ./

# RUN chmod +x run_app.sh

# ENTRYPOINT [ "/app/run_app.sh" ]

CMD ["gunicorn", "foodgram_backend.wsgi:application", "--bind", "0:8000"] 
