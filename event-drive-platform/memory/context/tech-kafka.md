---
type: concept
id: tech-kafka
title: Apache Kafka 4.x (KRaft)
sources:
- docs/ADR-001-architecture-approach.md
---

# Apache Kafka 4.x (KRaft)

Лог-брокер для ядра и регионов. Apache 2.0, ZooKeeper убран в 4.0 (2025-03). По умолчанию `acks=all` не делает fsync перед ответом.
