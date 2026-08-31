# Architecture

## Data flow

```
Python producer (Faker)
      │  writes to
      ▼
Kafka topics: orders, clickstream        (Docker: confluentinc/cp-kafka)
      │  consumed by
      ▼
Python consumer (batches, partitions by date)
      │  writes to
      ▼
MinIO bucket: raw-events                  (S3-compatible, local)
      │  detected by
      ▼
Airflow DAG: load_raw_to_snowflake
      │  PUT + COPY INTO (internal stage)
      ▼
Snowflake: RAW schema
      │  dbt run
      ▼
Snowflake: STAGING schema → MARTS schema  (fct_orders, fct_sessions, dim_customers, dim_products)
      │
      ▼
Metabase dashboards + dbt tests/docs, GitHub Actions CI on every PR
```

## Why an internal stage instead of an external S3 stage

Snowflake is a cloud SaaS — it cannot reach a `localhost` MinIO bucket
directly. Rather than exposing MinIO to the internet or paying for real AWS
S3, the Airflow DAG pulls files from MinIO and pushes them into Snowflake via
a **named internal stage** (`PUT` + `COPY INTO`). This keeps every other
component free/local while still exercising the real "object storage landing
zone → warehouse load" pattern.

## Schema layers (Snowflake)

- `RAW` — as-landed data from `COPY INTO`, minimal typing
- `STAGING` — dbt staging models: renamed/typed/deduplicated, 1:1 with raw sources
- `MARTS` — dbt marts: `fct_orders`, `fct_sessions`, `dim_customers`, `dim_products`

## Build plan

See the root `README.md` for the week-by-week checklist.
