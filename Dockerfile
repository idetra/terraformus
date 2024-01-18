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

# Copy Nginx configuration
COPY --from=build /app/nginx/conf.d/ /etc/nginx/conf.d/terraformus

# Copy Django application
COPY --from=build /app /app

WORKDIR /app

# Expose port 8000 for the Django application
EXPOSE 8000

# Start Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

