---
type: concept
id: concept-k-event
title: Категория K — критичные события
sources:
- docs/eda-platform-requirements.md
---

# Категория K — критичные события

Команды действия: запуск процессов, модификация данных, любое изменение состояния объектов модели. Не теряются и не вытесняются, [[validity-window]] 48 ч, подтверждение по [[durable-journal|локальной durable-записи]].
