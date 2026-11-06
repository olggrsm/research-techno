---
type: insight
id: tension-5
title: Exactly-once и границы системы
sources:
- docs/eda-platform-requirements.md
---

# Напряжение 5: Exactly-once и границы системы

Exactly-once внутри брокера не распространяется на БД и внешние системы. Практичный путь — at-least-once плюс идемпотентность плюс outbox.

## Затронутые требования

- (нет прямых ссылок)
