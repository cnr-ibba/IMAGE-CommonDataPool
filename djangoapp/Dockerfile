 FROM python:3.8

 RUN mkdir /code
 WORKDIR /code

 COPY ./requirements.txt /code
 RUN pip install -r requirements.txt

 EXPOSE 8000
 CMD ["gunicorn", "--bind", ":8000", "api_service.wsgi:application"]
