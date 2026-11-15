---
type: insight
id: tension-3
title: Автономность и согласованность
sources:
- docs/eda-platform-requirements.md
- docs/adr/0008-requirement-tensions.md
---

# Напряжение 3: Автономность и согласованность

Во время разделения доступны только eventual или causal модели. Глобальный порядок и linearizable операции недоступны.

## Затронутые требования

- (нет прямых ссылок)

## Решение каталога

Не снимается решением: каждый класс данных объявляет модель согласованности (R-11) — см. `docs/adr/0008-requirement-tensions.md`.
