<div align="center">

[![Platform and backend engineering — building observable AI systems](assets/platform-engineering-banner.gif)](https://syedtashfin.com/case-studies/cicd-gitops-multitenant-kubernetes-saas)

# Syed Mohammad Shah Mostafa (Tash)

### Platform & Backend Engineer — building observable AI systems

Paris, France · Targeting English-speaking platform, backend, cloud and AI-platform roles

[Portfolio](https://syedtashfin.com) · [Engineering brief](assets/from-commit-to-observable-rollback.pdf) · [Case studies](https://syedtashfin.com/case-studies) · [LinkedIn](https://www.linkedin.com/in/syed-mostafa) · [Email](mailto:syed@syedtashfin.com)

</div>

## What I do

I build the part of the stack people rely on after launch — backend services, CI/CD and GitOps delivery, Kubernetes controls, telemetry, and bounded AI workflows. Everything I ship moves along one path, so it can be reviewed, released, observed and rolled back:

```text
code → tests → immutable artifact → reviewed GitOps → runtime → telemetry → rollback
```

My public work is grouped below by domain; each project is labeled by scope so the evidence stays honest.

## Platform & delivery

| Project | Scope | Engineering signal |
| --- | --- | --- |
| [Multi-Tenant GitOps Platform Lab](https://github.com/SyedTashfin/Outsight-MultiTenant-GitOps-Lab) | Production-style lab | GitHub Actions, multi-arch GHCR images, Helm overlays, Argo CD reconciliation, Prometheus-gated Argo Rollouts, RBAC, NetworkPolicy, Grafana + Loki. [Case study](https://syedtashfin.com/case-studies/cicd-gitops-multitenant-kubernetes-saas) |
| [Cloud Analytics ML Pipeline](https://github.com/SyedTashfin/Cloud-Analytics-ML-Pipeline) | Production-style data lab | Config-driven PySpark ingestion, feature engineering, MLlib training/evaluation, dashboard artifacts, local-to-GCP Dataproc parity. |
| LC production infrastructure | Employer org — documented | WordPress → versioned Next.js/TypeScript catalogue (299 SSG pages), separate staging/prod GitHub Actions paths on one VPS, incident recovery. Covered in the [engineering brief](assets/from-commit-to-observable-rollback.pdf). |

## Backend & AI systems

| Project | Scope | Engineering signal |
| --- | --- | --- |
| [Thales Optronic Video Indexing](https://github.com/SyedTashfin/Thales-optronic-video-indexing) | Academic collaboration | FastAPI, Celery/Redis, frame sampling, YOLO, OCR, Whisper transcription, semantic search, JSON/PDF/CSV reporting. |
| [Local Multi-LLM Orchestrator](https://github.com/SyedTashfin/Local-Multi-LLM-Orchestrator) | Personal systems project | Local Ollama services, anonymized peer review, chairman synthesis, strict JSON/Zod contracts, SQLite run history, health/latency observability. |

## Security engineering

| Project | Scope | Engineering signal |
| --- | --- | --- |
| [ISO 27001 Lab](https://github.com/SyedTashfin/ISO-27001-Web-App) | Deployed learning product | Bilingual Next.js platform for evidence, risk treatment, SoA, audit, nonconformity, Annex A controls, mock-exam practice. |
| [Lightweight Authentication for LIN/CAN Probes](https://github.com/SyedTashfin/Lightweight-Authentication-for-LIN-CAN-Probes) | Research prototype | Message-authentication scheme for automotive LIN/CAN buses. |
| [Bangladesh E-Voting](https://github.com/SyedTashfin/Bangladesh-E-Voting) | Research prototype | Blockchain e-voting with Solidity, React and Web3.js — cast-as-intended integrity. |

## Products & apps

| Project | Scope | Engineering signal |
| --- | --- | --- |
| [ATouPay](https://github.com/SyedTashfin/AtouPay) | Product MVP | Expo/React Native client, Fastify API, Firebase identity/data, backend-owned critical writes, receipts, recovery, provider boundary for payments. |
| [SyntaxMap](https://github.com/SyedTashfin/Syntax-Map-Original) | Teaching product | Interactive classroom tool for English grammar practice, built and used at Linguistic Communication. |
| [Fit Paris Flow](https://github.com/SyedTashfin/fit-paris-flow) | Product prototype | Fitness-scheduling web app (TypeScript, Vercel). |

## Open-source

Early in the contribution cycle — I am transparent that no upstream merge has landed yet. What exists is verifiable in-progress work on flagship projects:

- **[OpenTelemetry JS contrib PR #3669](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/3669)** — deprecation of the long-task instrumentation, reviewed by a maintainer, who asked for the replacement (`Long Animation Frames`) to be built first. I am building that replacement now. CLA signed, not merged.
- **[Grafana MCP #987](https://github.com/grafana/mcp-grafana/issues/987)** — traced a service-account token-rotation bug across stdio and HTTP client lifecycles and proposed maintainer-reviewable implementation paths.

My process: reproduce the issue → propose a focused change → sign the CLA → iterate with maintainers → land. I log scope honestly so nothing is presented as merged before it is.

## Security hardening (LC production, ESILV internship)

A proportionate security baseline applied to Linguistic Communication's public Next.js platform, validated in staging then production:

- **Retired the live HTML uploader** in favour of Git-reviewed publication.
- **Sandboxed embedded content** without `allow-same-origin`.
- **Bounded the two lead APIs** (`quiz-lead`, `b2b-diagnostic-lead`): content-type checks, 64 KB body cap, field/array limits.
- **Bot and abuse controls:** honeypot, minimum completion time, short-window duplicate suppression, SMTP rate limits.
- **Edge identity and headers:** trusted client-IP restoration behind Cloudflare, baseline security headers, CSP report-only, disabled `X-Powered-By`, Nginx body/rate limits, `security.txt` + data-handling policy.
- **Evidence:** a baseline-vs-hardened scenario harness (13/13 hardened tests pass; primary runtime/static classes 1/14 → 14/14) plus staging and production validation.

## Engineering focus

| Platform delivery | Backend systems | Observability & AI |
| --- | --- | --- |
| Linux · Docker · Kubernetes · Helm · Argo CD · GitHub Actions | TypeScript · Python · FastAPI · Fastify · PostgreSQL | OpenTelemetry · Prometheus · Grafana · LangGraph · RAG · pgvector |

## Useful review paths

- **Platform / cloud:** the [six-page engineering brief](assets/from-commit-to-observable-rollback.pdf), then the [GitOps case study](https://syedtashfin.com/case-studies/cicd-gitops-multitenant-kubernetes-saas).
- **Backend / AI systems:** [Thales Video Indexing](https://github.com/SyedTashfin/Thales-optronic-video-indexing) and the [Local Multi-LLM Orchestrator](https://github.com/SyedTashfin/Local-Multi-LLM-Orchestrator).
- **Security-aware engineering:** [ISO 27001 Lab](https://github.com/SyedTashfin/ISO-27001-Web-App) and the [LC production hardening](#security-hardening-lc-production-esilv-internship) above.
- **Broader evidence:** the [portfolio evidence map](https://syedtashfin.com/evidence-map).

<div align="center">

![Contribution activity](https://raw.githubusercontent.com/SyedTashfin/SyedTashfin/output/github-contribution-grid-snake.svg)

</div>
