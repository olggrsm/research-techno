---
type: concept
id: durable-journal
title: Durable-журнал
sources:
- docs/eda-platform-requirements.md
---

# Durable-журнал

Локальный журнал на N1–N3 с документированной политикой fsync. Подтверждение выдаётся только после fsync или кворумной записи; режим «flush раз в N секунд» для [[concept-k-event|K]] запрещён.
