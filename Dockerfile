FROM python:3.10.6-slim-buster

WORKDIR /app

LABEL maintainer="Co-Bersih"
LABEL description="Development image for the Co-Bersih API"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean

RUN apt-get update \
    && apt-get install -y binutils libproj-dev gdal-bin python-gdal python3-gdal

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

RUN sleep 8 && python3 manage.py migrate && echo "from apps.user.models import User; User.objects.create_superuser(email='administrator@mail.com', password='administrator')" | python3 manage.py shell

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]