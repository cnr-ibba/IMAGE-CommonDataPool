 FROM python:3

 RUN mkdir /code
 WORKDIR /code

 COPY ./requirements.txt /code
 RUN pip install -r requirements.txt

 COPY . /code
 RUN python manage.py collectstatic --no-input

 EXPOSE 8000
 CMD ["gunicorn", "--bind", ":8000", "api_service.wsgi:application"]