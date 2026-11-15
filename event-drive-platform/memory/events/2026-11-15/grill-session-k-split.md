---
type: event
id: grill-session-k-split-2026-11-15
summary: Грилинг по клиппингу eda-principals.md; K разделён на команды и факты, приняты SLO, T_revoke, догонка по изоляции, 10 ADR
occurred_at: '2026-11-15T14:30:00+03:00'
entities:
- platform
- k-event
- k-command
- k-fact
- node-n0
- node-n1
- node-n2
- node-n3
- replication
sources:
- Clippings/eda-principals.md
- docs/eda-platform-requirements.md
- docs/adr/0001-split-k-commands-and-facts.md
- docs/adr/0002-mixed-durability-and-replication.md
- docs/adr/0003-event-bus-technology.md
- docs/adr/0004-k-capacity-and-catchup.md
- docs/adr/0005-trust-and-policy-under-isolation.md
- docs/adr/domain/0001-idempotency-and-aggregate-version.md
derived_facts:
- memory/facts/k-command/k-command-rate.md
- memory/facts/k-fact/k-fact-rate.md
- memory/facts/replication/catchup-by-isolation.md
---

# Грилинг по клиппингу и фиксация решений

Разобран `Clippings/eda-principals.md`. Ключевое решение: K делится на [[concept-k-command|K-команду]] и [[concept-k-fact|K-факт]] (ADR-0001), потоки разделены пространствами имён `k.cmd.>` и `k.fact.>` в пропорции 1 к 10. Рекомендация клиппинга «RF ≥ 3, min.insync.replicas = 2» принята только для N3, на N1 и N2 действует смешанный режим ADR-0002.

Приняты: p99 для команд 20 мс локально и 200 мс между соседями, для фактов 50 мс; T_revoke 15 мин; догонка 2 ч при изоляции до 6 ч (канал 4r), 8 ч при 24 ч, 16 ч при 48 ч; срок хранения записи об истечении 10 ч; N0 — устройство без диска, K не порождает; требований по суверенитету данных нет.

Темы клиппинга (bi-temporal, CQRS/ES, партиционирование) отнесены к доменным ADR — `docs/adr/domain/`.
