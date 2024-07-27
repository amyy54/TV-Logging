FROM python:3.12

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install gunicorn~=22.0.0
RUN pip install -r requirements.txt

COPY . /code

RUN DEBUG=0 python3 manage.py collectstatic --noinput

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "django_project.wsgi:application"]
