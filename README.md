# IMAGE-CommonDataPool
IMAGE Common Data Pool - PostgreSQL, metadata structure and data loading scripts

# Runing app
Create migrations:

```docker-compose run web ./manage.py makemigrations```

Apply migrations:

 ```docker-compose run web ./manage.py migrate```
 
Run app:

```docker-compose up```

Upload test data:

```python ./import_test_data.py```

Stop app:

```docker-compose down```

 
