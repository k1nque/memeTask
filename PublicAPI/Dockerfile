FROM python:3.10

ENV PYTHONBUFFERED=1

WORKDIR /PublicAPI

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
