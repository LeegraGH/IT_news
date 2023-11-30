FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM python:3.9-slim-bullseye

WORKDIR /project

#ENV PYTHONDONTWRITEBYTECODE=1 \
#    PYTHONBUFFERED=1
#
#COPY . .
#
#RUN apt-get update && apt-get install --no-install-recommends -y \
#    gcc libc-dev libpq-dev  python-dev libxml2-dev libxslt1-dev python3-lxml && apt-get install -y cron &&\
#    pip install --no-cache-dir -r requirements.txt
