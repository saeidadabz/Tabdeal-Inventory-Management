
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip -i https://package-mirror.liara.ir/repository/pypi/simple
RUN pip install -r requirements.txt -i https://package-mirror.liara.ir/repository/pypi/simple

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
