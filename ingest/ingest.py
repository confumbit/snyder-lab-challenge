import wearipedia
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

LAST_RUN_FILE = "/app/ingest/last_run.txt"


def get_last_run():
    try:
        with open(LAST_RUN_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return datetime.utcnow().strftime("%Y-%m-%d")


def update_last_run(timestamp):
    with open(LAST_RUN_FILE, "w") as f:
        f.write(timestamp)


def fetch_fitbit_data(start_date):
    START_DATE = "2024-12-01"  # @param {type:"string"}
    END_DATE = "2024-12-10"  # @param {type:"string"}
    params = {"seed": 100, "start_date": START_DATE, "end_date": END_DATE}
    device = wearipedia.get_device("fitbit/fitbit_charge_6")
    br = device.get_data("intraday_breath_rate", params)
    azm = device.get_data("intraday_active_zone_minute", params)
    activity = device.get_data("intraday_activity", params)
    hr = device.get_data("intraday_heart_rate", params)
    hrv = device.get_data("intraday_hrv", params)
    spo2 = device.get_data("intraday_spo2", params)
    return hr


def ingest_to_db(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Create hypertable if not exists
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS raw_data (
            timestamp TIMESTAMPTZ PRIMARY KEY,
            value INTEGER
        );
        SELECT create_hypertable('raw_data', 'timestamp', if_not_exists => TRUE);
    """
    )

    # In actual use, we will only take the last day's data since our cron job runs daily.
    # Each new day has completely new data removing the necessity of using the otherwise more efficient UPSERT query.
    for day in data:
        datapoints = day["heart_rate_day"][0]["activities-heart-intraday"]["dataset"]
        date = day["heart_rate_day"][0]["activities-heart"][0]["dateTime"]
        for point in datapoints:
            timestamp = f"{date} {point['time']}"
            cur.execute(
                """
                INSERT INTO raw_data (timestamp, value)
                VALUES (%s, %s)
                ON CONFLICT (timestamp) DO NOTHING;
            """,
                (timestamp, float(point["value"])),
            )

    conn.commit()
    cur.close()
    conn.close()


def main():
    last_run = get_last_run()
    print(f"Fetching Fitbit data for: {last_run}")
    data = fetch_fitbit_data(last_run)
    ingest_to_db(data)
    update_last_run(datetime.utcnow().strftime("%Y-%m-%d"))


if __name__ == "__main__":
    main()
