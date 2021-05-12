# Airflow Demo

## Starting Airflow Server
```
1. mkdir ./logs ./plugins
2. docker-compose up airflow-init
3. docker-compose up
```

## Clean up
This will remove airflow and postgres docker images as well as the postgres docker volume.
```
docker-compose down --volumes --rmi all
```
