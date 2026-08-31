# DAGs

- `load_raw_to_snowflake` (Week 2): detects new MinIO files, `PUT`s them to a
  Snowflake internal stage, `COPY INTO` raw tables.
- `run_dbt_models` (Week 2): runs `dbt run` + `dbt test` after a successful load.

Not yet implemented.
