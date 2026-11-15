---
type: concept
id: tech-nats-jetstream
title: NATS JetStream + leaf nodes
sources:
- docs/adr/0003-event-bus-technology.md
---

# NATS JetStream + leaf nodes

Лёгкий брокер для края. Apache 2.0 (CNCF). Leaf сам открывает исходящее соединение. Jepsen 2.12.1: потери подтверждённых записей при ленивом fsync.
