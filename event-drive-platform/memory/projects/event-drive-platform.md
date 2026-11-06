---
type: project
id: event-drive-platform
title: Модель исследования event-driven платформы
sources:
- docs/eda-platform-requirements.md
---

# Модель исследования

Источник требований: `docs/eda-platform-requirements.md` (черновик от 2026-11-06).

## Концепции

- [[concept-platform|platform]] — Платформа
- [[node]] — Узел
- [[concept-node-n0|node-n0]] — N0 — конечное устройство
- [[concept-node-n1|node-n1]] — N1 — edge-узел
- [[concept-node-n2|node-n2]] — N2 — региональный узел
- [[concept-node-n3|node-n3]] — N3 — ядро
- [[vertical-link]] — Вертикальная связь
- [[horizontal-link]] — Горизонтальная связь
- [[concept-cell|cell]] — Ячейка (cell)
- [[store-and-forward]] — Store-and-forward
- [[event]] — Событие
- [[concept-k-event|k-event]] — Категория K — критичные события
- [[e-event]] — Категория E — прочие события
- [[event-class]] — Класс события
- [[durable-journal]] — Durable-журнал
- [[concept-replication|replication]] — Репликация
- [[k-reserve]] — Резерв под K
- [[expiry-record]] — Запись об истечении
- [[hlc]] — HLC-метка
- [[cloudevents]] — CloudEvents
- [[idempotency-key]] — Идемпотентный ключ
- [[single-writer]] — Single-writer — узел-владелец
- [[validity-window]] — Срок актуальности K
- [[autonomy-window]] — T_aut — окно автономности
- [[backpressure]] — Backpressure
- [[latency-budget]] — Latency budget
- [[schema-registry]] — Schema registry
- [[event-catalog]] — Каталог событий
- [[dlq]] — DLQ

## Требования (P — быстродействие, R — живучесть, D — развёртывание, X — сквозные)

- [[p-1]] — MUST
- [[p-2]] — MUST
- [[p-3]] — MUST
- [[p-4]] — MUST
- [[p-5]] — MUST
- [[p-6]] — MUST
- [[p-7]] — MUST
- [[p-8]] — MUST
- [[p-9]] — SHOULD
- [[p-10]] — MUST
- [[p-11]] — MUST
- [[r-1]] — MUST
- [[r-2]] — MUST
- [[r-3]] — MUST
- [[r-4]] — MUST
- [[r-5]] — MUST
- [[r-6]] — MUST
- [[r-7]] — MUST
- [[r-8]] — MUST
- [[r-9]] — MUST
- [[r-10]] — MUST
- [[r-11]] — MUST
- [[r-12]] — SHOULD
- [[r-13]] — MUST
- [[r-14]] — MUST
- [[r-15]] — MUST
- [[r-16]] — MUST
- [[r-17]] — MUST
- [[r-18]] — MUST
- [[d-1]] — MUST
- [[d-2]] — MUST
- [[d-3]] — MUST
- [[d-4]] — MUST
- [[d-5]] — MUST
- [[d-6]] — MUST
- [[d-7]] — SHOULD
- [[d-8]] — MUST
- [[d-9]] — MUST
- [[x-1]] — MUST
- [[x-2]] — MUST
- [[x-3]] — MUST
- [[x-4]] — SHOULD
- [[x-5]] — MUST
- [[x-6]] — MUST
- [[x-7]] — MUST
- [[x-8]] — MUST
- [[x-9]] — MUST
- [[x-10]] — SHOULD
- [[x-11]] — SHOULD
- [[x-12]] — SHOULD

## Напряжения

- [[tension-1]] — Долговечность и задержка
- [[tension-2]] — Автономность и безопасность
- [[tension-3]] — Автономность и согласованность
- [[tension-4]] — Порядок и масштаб
- [[tension-5]] — Exactly-once и границы системы
- [[tension-6]] — Ёмкость и длительность изоляции
- [[tension-7]] — P2P-обмен и долговечный журнал
- [[tension-8]] — Команды K и актуальность
- [[tension-9]] — Команды K на обеих сторонах разделения
