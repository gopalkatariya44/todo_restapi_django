```shell
python manage.py startapp todo
```

```shell
python manage.py makemigrations
python manage.py migrate
```

curl -X GET http://127.0.0.1:8000/api/v1/task?format=json \
-H "Authorization: Token 4183a827119c757a4c3d7c9cb06354657dcb7ede"



