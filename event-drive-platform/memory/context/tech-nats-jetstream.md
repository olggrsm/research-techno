---
type: concept
id: tech-nats-jetstream
title: NATS JetStream + leaf nodes
sources:
- docs/ADR-001-architecture-approach.md
---

# NATS JetStream + leaf nodes

Лёгкий брокер для края. Apache 2.0 (CNCF). Leaf сам открывает исходящее соединение. Jepsen 2.12.1: потери подтверждённых записей при ленивом fsync.
