# IMAGE-CommonDataPool
IMAGE Common Data Pool - PostgreSQL, metadata structure and data loading scripts

# Runing app


Create migrations:

```docker-compose run web ./manage.py makemigrations```

Apply migrations:

 ```docker-compose run web ./manage.py migrate```
 
Run app:

```docker-compose up```

Create superuser:

```docker-compose run web ./manage.py createsuperuser --email {your email} --username admin```

Upload test data:

```python ./import_test_data.py {admin password}```

Stop app:

```docker-compose down```

 
