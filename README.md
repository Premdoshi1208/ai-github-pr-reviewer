# PR Autopilot — Multi-Agent GitHub Code Review System

> Autonomous AI system that reviews every Pull Request using 4 specialized agents running in parallel — catching bugs, security vulnerabilities, style issues, and architecture problems before they reach production.

---

## What It Does

When a developer opens a Pull Request, this system automatically:

1. Receives the GitHub webhook event
2. Fetches the code diff
3. Runs **4 AI agents in parallel** to analyze the code
4. Posts **inline review comments** directly on the PR within seconds
5. Learns from merged PRs to improve future reviews

No human needs to trigger it. No manual steps. Fully autonomous.

---

## Architecture

```
GitHub PR Created
        │
        ▼
  AWS Load Balancer
        │
        ▼
  Gateway Service         ← HMAC SHA-256 webhook verification
        │
        ▼
  Webhook Service         ← Parses PR metadata, queues job to Redis
        │
        ▼
  Celery Worker           ← Async background processing
        │
        ▼
  Orchestrator Service    ← Fetches code diff, runs LangGraph agents
        │
   ┌────┴────┬──────────────┬────────────────┐
   ▼         ▼              ▼                ▼
Static    Security        Style         Architecture
Analysis   Agent          Agent            Agent
Agent
   └────┬────┴──────────────┴────────────────┘
        │
        ▼
  Reviewer Service        ← Posts inline comments to GitHub PR
        │
        ▼
  [On Merge] Learner      ← Stores patterns in PostgreSQL for future reviews
```

**5 Microservices** · **4 Parallel AI Agents** · **Async Processing** · **Self-Improving**

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Orchestration | LangGraph, OpenAI GPT-4o-mini |
| Backend | FastAPI, Celery, SQLAlchemy, Alembic |
| Queue / Cache | Redis (AWS ElastiCache) |
| Database | PostgreSQL 15 (AWS RDS) |
| Infrastructure | AWS EKS, ECR, S3, Terraform |
| CI/CD | GitHub Actions (5 independent pipelines) |
| Observability | Prometheus, Grafana, Langfuse |
| Evaluation | RAGAS (weekly automated LLM quality scoring) |
| Auth | HMAC SHA-256, PyJWT, GitHub App |

---

## The 4 AI Agents

| Agent | What It Catches |
|---|---|
| **Static Analysis** | Code complexity, unused variables, bad naming, logic bugs |
| **Security** | OWASP Top 10, hardcoded secrets, SQL injection, eval() abuse |
| **Style** | Formatting, readability, PEP8 violations |
| **Architecture** | Separation of concerns, missing error handling, design flaws |

All 4 agents run in **parallel** via LangGraph, not sequentially — minimizing latency.

---

## Key Features

- **Fully autonomous** — triggered by GitHub webhook, no manual steps
- **Parallel agent execution** — LangGraph orchestrates all 4 agents simultaneously
- **Self-improving** — Learner service captures patterns from merged PRs
- **Production observability** — Prometheus metrics + Grafana dashboards per service
- **LLM tracing** — every agent call traced in Langfuse with token count, latency, cost
- **Automated evaluation** — RAGAS runs weekly to score faithfulness and answer relevancy
- **5 independent CI/CD pipelines** — changing one service deploys only that service
- **Kubernetes autoscaling** — HPA on orchestrator scales with load

---

## System Demo

**Input — test code opened as a PR:**
```python
def calculate(a, b):
    password = "admin123"
    result = eval(a + b)
    return result
```

**Output — bot posts inline comments automatically:**
- 🔴 **Security**: Hardcoded password detected on line 2 — use environment variables
- 🔴 **Security**: `eval()` on user input is a critical code injection vulnerability
- 🟡 **Style**: Missing type annotations and docstring
- 🟡 **Architecture**: No input validation or error handling

---

## Project Structure

```
ai-code-reviewer/
├── services/
│   ├── gateway/          # Webhook verification
│   ├── webhook/          # Event parsing + job queuing
│   ├── orchestrator/     # LangGraph agent orchestration
│   ├── reviewer/         # GitHub comment posting
│   └── learner/          # Pattern learning post-merge
├── infra/
│   ├── terraform/        # AWS infrastructure as code
│   └── k8s/              # Kubernetes manifests
├── monitoring/
│   ├── prometheus.yml    # Scrape config for all 5 services
│   └── grafana-dashboard.json
├── scripts/
│   └── evaluate.py       # Weekly RAGAS evaluation
└── .github/workflows/    # 5 CI/CD pipelines + 1 eval pipeline
```

---

## CI/CD

5 independent GitHub Actions pipelines — one per service. Each has 3 jobs:

```
test → build-and-push → deploy
```

Pushing a change to `services/orchestrator/` triggers **only** the orchestrator pipeline. The other 4 services are untouched. Deployment uses OIDC (no long-lived AWS credentials stored in GitHub).

---

## Observability

- **Grafana** — request rate, p99 latency, error rate per service (auto-refreshes every 30s)
- **Prometheus** — raw metrics scraping all 5 services
- **Langfuse** — full LLM trace per PR: prompt, response, tokens, cost, latency per agent span
- **RAGAS eval** — automated weekly job scores faithfulness ≥ 0.7 or pipeline fails

---

## Infrastructure Cost

Running fully on AWS at ~$179/month (2x EKS nodes, RDS, ElastiCache, ALB).
Teardown with `terraform destroy` — zero ongoing charges.
