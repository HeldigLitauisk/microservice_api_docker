Microservice API running on Flask webserver with postgreSQL db on docker instance

1. Start by running:
```
docker-compose build && docker-compose up -d
```

2. Run tests:
```
python3 -m pytest ./test_payloads.py
```