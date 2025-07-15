Task 0 a can be found in task0a.md

Task 0 b is performed in conjuction with Task 1 and specifically can be found in the `fetch_fitbit_data` function in `ingest/ingest.py`

## Task 1

### Fitbit to TimescaleDB Ingestion Pipeline

This pipeline pulls intraday Fitbit data daily and stores it in a local TimescaleDB instance using Docker Compose.

- **TimescaleDB**: Time-series database to store heart rate metrics.
- **Python Ingestor**: Scheduled via cron to run daily at 1 AM.
- **Docker**: Manages both services.

#### Setup
To run:
   ```bash
   docker compose up --build
   ```


## Task 2