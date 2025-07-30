FROM python:3.11-slim

WORKDIR /app

COPY . . 

RUN pip install --no-cach-dir -r requirements.txt

EXPOSE 80

CMD ["python", "backend.py", "frontend.py"]