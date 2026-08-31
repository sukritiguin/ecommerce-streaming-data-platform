# E-Commerce Streaming Data Platform

An end-to-end data platform that simulates e-commerce orders and clickstream
events, streams them through Kafka, lands them in S3-compatible object
storage, orchestrates loading with Airflow, and models them in Snowflake with
dbt. Built to demonstrate the streaming-to-warehouse pattern (Kafka, Airflow,
Snowflake, dbt) on top of an AWS-flavored object storage layer.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full data flow
diagram and design rationale.

## Stack

| Layer | Tool |
|---|---|
| Streaming | Apache Kafka (Docker) |
| Object storage | MinIO (S3-compatible, local) |
| Orchestration | Apache Airflow |
| Warehouse | Snowflake |
| Transformation | dbt-core |
| BI | Metabase |
| CI | GitHub Actions |

## Prerequisites

- Docker + Docker Compose
- Python 3.10+
- A free [Snowflake trial account](https://signup.snowflake.com/) (needed from Week 2 onward)
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) — required to run the dbt/Snowflake MCP servers (`uvx ...`)

## Getting started

```bash
cp .env.example .env        # fill in values as you reach each step
make up                     # starts Kafka, MinIO, Postgres, Airflow
```

- Airflow UI: http://localhost:8080 (admin/admin)
- MinIO console: http://localhost:9001 (minioadmin/minioadmin)

`make down` stops the stack; `make reset` also wipes volumes.

## MCP integrations

Configured in [`.mcp.json`](.mcp.json) (project-scoped, checked into git — no
secrets in the file itself, only `${VAR}` references resolved from your shell
env / `.env`):

| Server | Purpose | Needs |
|---|---|---|
| `dbt` | Query/run the local dbt project (models, tests, docs) directly from Claude | `uv` installed; works once `dbt/` is initialized (Week 2) |
| `snowflake` | Query Snowflake objects/data directly from Claude | Snowflake trial credentials in `.env` (Week 2) — see [`snowflake/tools_config.yaml`](snowflake/tools_config.yaml) for the permission allowlist (Delete/Drop are off by default) |
| `github` | Manage issues/PRs on this repo directly from Claude | `GITHUB_PERSONAL_ACCESS_TOKEN` in `.env` — quickest way: `export GITHUB_PERSONAL_ACCESS_TOKEN=$(gh auth token)` |
| `notion` | Read/write project docs in Notion from Claude | Authenticates via OAuth on first use — no token needed |

Claude Code picks up `.mcp.json` automatically when you open this directory.
Restart your Claude Code session after editing `.env` for new credentials to
take effect.

## Build plan

**Week 1 — Ingestion foundation**
- [x] Repo scaffold, Docker Compose (Kafka, MinIO, Airflow), MCP config, git/GitHub
- [ ] Snowflake trial account: warehouse, database, raw/staging/marts schemas
- [ ] Python producer: simulate orders + clickstream events onto Kafka
- [ ] Python consumer: batch-write Kafka events to MinIO, partitioned by date

**Week 2 — Orchestration + modeling**
- [ ] Airflow DAG: MinIO → Snowflake internal stage → `COPY INTO` raw tables
- [ ] dbt project: staging models (`stg_orders`, `stg_clickstream`), marts (`fct_orders`, `fct_sessions`, `dim_customers`, `dim_products`)
- [ ] dbt tests wired into the Airflow DAG after load

**Week 3 — Productionizing**
- [ ] GitHub Actions CI: `dbt build` on every PR against a CI schema
- [ ] Data quality alerting (Airflow on-failure callback)
- [ ] Metabase dashboard (revenue trend, funnel conversion, top products)
- [ ] Final README polish + resume bullets
