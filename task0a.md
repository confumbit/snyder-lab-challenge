# Task 0.a

1.  a. 365 x 24 x 60 x 60 x 4 x n ~ 126 mil. seconds

    - n=1, 126 mil. datapoints
    - n=1000, 126 bil. datapoints
    - n=10000, 1260 bil. datapoints

1.  b.

    - 1 year, 126 mil. datapoints
    - 2 year, 252 mil. datapoints
    - 5 year, 630 mil. datapoints

1.  Taking heart_rate as double, steps as bigint, distance as double, spo2 as double and a timestamp

With the header for each tuple in postgres being 24 bytes, a single data point would add 16 bytes if we record the timestamp for each data point or only 8 bytes (24 bytes for header and 8 bytes for timestamp) if we record the timestamp only once in a row containing all the recorded metrics at that timestamp.

Assuming, we recieve all the metrics at the same time, 1 row with 4 data points would take (in bytes):
24 (header) + 8\*5 (metrics + timestamp) = 64 bytes

Taking a smaller data type for any metric does not help since postgres would pad it to make it 8 bytes.

for n = 1000, this is 62.5 kB every second
for 2 years and n= 1, this is 62.5 x 365 x 24 x 60 x 60 ~ 1880 MB

with 3 metrics this comes to

# Task 0.a

## 1. Estimating Data Points

Assume we collect 4 metrics (`heart_rate`, `steps`, `distance`, `spo2`) at **1-second resolution**.

### a.

- **Seconds per year**:  
  365 days × 24 hours × 60 minutes × 60 seconds = `31,536,000` seconds
- **Data points per year per person**:  
  `31,536,000 × 4 metrics = 126,144,000`

| n (participants) | Total Data Points |
| ---------------- | ----------------- |
| 1                | 126,144,000       |
| 1,000            | 126,144,000,000   |
| 10,000           | 1,261,440,000,000 |

### b.

| Duration | Data Points (per person) |
| -------- | ------------------------ |
| 1 year   | 126.1 million            |
| 2 years  | 252.3 million            |
| 5 years  | 630.7 million            |

---

## 2. Storage Estimation

### a.

Taking `heart_rate` as double, `steps` as bigint, `distance` as double, `spo2` as double and a `timestamp`, and `source_id` as bigint

Estimate per data point:

24 bytes (page header) + 8 bytes x (2 + 1) (data point for timestamp + source_id, metric) = **48 bytes**

### a. Uncompressed storage for n = 1,000, 2 years, 3 metrics

Storing the 3 metrics in a single record,

- record/row size = 24 + 8 x (2 + 3) = **64 bytes**
- Seconds in 2 years = 63,072,000
- Size of rows per person in 2 years = 63,072,000 x 64 = 4,036,608,000 bytes
- Taking (1 kB = 1024 bytes and so on) = 3.76 GB
- For 1,000 people:  
  `3.76 × 1,000 = 3760 GB =` **`3.67 TB`** is the uncompressed size in postgres.

### b. Compressed storage at 80% compression

- Compressed size = 20% of 3.67 TB = **~751 GB**

#### i. How can time-series databases compress data so much?

**Compression techniques:**

- Delta encoding (store differences between values)
- Run-length encoding (store repeated values)
- Dictionary encoding (for repeated tags)
- Segment-level metadata reduction

**When compression is effective:**

- Gradual, periodic, or predictable changes (e.g., heart rate, steps)
- Low-entropy data

**When compression is poor:**

- Highly volatile or random data

**Fitbit data is a good compression candidate because most metrics (heart rate, steps, sleep) show gradual trends or repeated patterns.**

---

## 3. Realistic Metric Frequencies from Fitbit API

### a. Relevant Metrics for a Physical Activity Affecting Sleep Study

| Metric                              | Max Frequency |
| ----------------------------------- | ------------- |
| Heart rate                          | 1 second      |
| Heart rate variability              | 1 day         |
| SpO2                                | 1 day         |
| Avg. breating rate / sleeping stage | 1 day         |
| Activity zone minutes               | 1 minute      |

### b. Actual data volume for n = 1,000 for 1 year

- row size = 24 + 8 x (2+5) = 80 bytes
- volume in 1 year per source = 365 x 24 x 60 x 60 x 80 ~ 2.35 GB
- for n = 1,000, 2.35 x 1000 = 2350 GB ~ 2.3 TB
- **Total uncompressed volume = 2.3 TB**

### c. Compressed (80%)

**2.3 x 0.2 = 471 GB**

---

## 4. Querying High-Resolution Time-Series Data

Some possible ways of getting faster and less expensive queries

- **Downsampling**: Precompute lower-resolution summaries (e.g., 1-min averages)
- **Materialized views**: Store common aggregations for faster retrieval
- **Chunking**: Partition data by time ranges
- **Efficient indexing**: Index by time and tags
- **Compression-aware scans**: Use columnar storage to skip irrelevant blocks

---

## 5. Vertical vs Horizontal Scaling

### a. Feasible Limits for Vertical Scaling (Single Server)

| Resource | Typical Limit       |
| -------- | ------------------- |
| CPU      | 32–64 cores         |
| RAM      | 512 GB – 1 TB       |
| Storage  | 10–40 TB (SSD/NVMe) |

**Constraints:**

- Disk I/O limits
- Memory bottlenecks
- Compute limits for large queries

### b. Horizontal Scaling (On-Premise, No Cloud)

**Strategies:**

- **User-based sharding**: Divide data by user ID range across machines
- **Time-based partitioning**: Split datasets by year/month

**Query Coordination:**

- Implement a **query router** to send/merge queries across nodes
- Use **caching** for repeated queries
- Ensure **clock synchronization** and **LAN-based communication**

**Additional Considerations:**

- Centralized logging and monitoring
- Data redundancy and backups
- Load balancing to avoid hotspots

---