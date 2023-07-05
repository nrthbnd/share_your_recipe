FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
# COPY backend/foodgram_backend/requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

# COPY backend/foodgram_backend/ ./
COPY . .

# RUN chmod +x run_app.sh

# ENTRYPOINT [ "/app/run_app.sh" ]

# CMD ["gunicorn", "foodgram_backend.wsgi:application", "--bind", "0:8000"] 
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram_backend.wsgi"]