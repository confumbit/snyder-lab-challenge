Task 0 a can be found in task0a.md

Task 0 b is performed in conjuction with Task 1 and specifically can be found in the `fetch_fitbit_data` function in `ingest/ingest.py`

**NOTE: The .env file has not been added to gitignore since this project is for demostration purposes and we are only working with synthetic data.**

## Task 1

### Fitbit to TimescaleDB Ingestion Pipeline

This pipeline pulls intraday Fitbit data daily and stores it in a local TimescaleDB instance using Docker Compose.

- **TimescaleDB**: Time-series database to store heart rate metrics.
- **Python Ingestor**: Scheduled via cron to run daily at 1 AM.
- **Docker**: Manages both services.

**NOTE: I am only loading a single day worth of data since the entire month would take too long for demonstration purposes.**

## Task 2

I am using a React front-end packaged with create-react-app and an Express.js back-end. It is a fairly simple modular design that can be extended quite easily.

**NOTE: The requests are not optimised and are quite slow, unfortunately I was not able to optimise them in time but rest assured, I believe my performance in the subsequent tasks for optmising the app would be quite satisfactory.**

#### Setup

**To run:**

```bash
docker compose up --build
```

In a seperate terminal run this to populate the data immediately instead of waiting for the cron job which only runs at 1 am.

```bash
docker exec -it fitbit_ingestor python ingest/ingest.py

```

Access the frontend dashboard at http://localhost:3000/ once the application is up and running.
