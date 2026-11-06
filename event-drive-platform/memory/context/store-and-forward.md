---
type: concept
id: store-and-forward
title: Store-and-forward
sources:
- docs/eda-platform-requirements.md
---

# Store-and-forward

Узел принимает и хранит события при отсутствии связи и передаёт их после восстановления, с дедупликацией по [[idempotency-key]].
