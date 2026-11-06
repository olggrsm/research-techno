---
type: concept
id: single-writer
title: Single-writer — узел-владелец
sources:
- docs/eda-platform-requirements.md
---

# Single-writer — узел-владелец

Единственный узел-владелец объекта модели; команды [[concept-k-event|K]] маршрутизируются владельцу, при его недоступности ждут в durable-очереди и не применяются на других узлах.
