# dbt project

Will be initialized in Week 2 with `dbt init` (adapter: `dbt-snowflake`).

Planned model layers:
- `staging/` — `stg_orders`, `stg_clickstream` (1:1 with raw tables, light cleanup)
- `marts/` — `fct_orders`, `fct_sessions`, `dim_customers`, `dim_products`
