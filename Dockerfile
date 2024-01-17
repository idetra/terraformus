# Stage 1: Build environment
FROM python:3.10-slim AS build

RUN apt update

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

# Stage 2: Production environment
FROM nginx:latest

COPY --from=build /app/nginx/conf.d/ /etc/nginx/conf.d/terraformus
COPY --from=build /app /app

WORKDIR /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

