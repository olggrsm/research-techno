---
type: insight
id: tension-7
title: P2P-обмен и долговечный журнал
sources:
- docs/eda-platform-requirements.md
- docs/adr/0008-requirement-tensions.md
---

# Напряжение 7: P2P-обмен и долговечный журнал

Peer-to-peer системы (Zenoh) хорошо дают горизонтальные связи, но гарантии долговечности у них в исследовании не проверены [?]. Для событий, которые нельзя потерять, нужен durable-журнал рядом с узлом.

## Затронутые требования

- (нет прямых ссылок)

## Решение каталога

Снимается ADR-0007 — см. `docs/adr/0008-requirement-tensions.md`.
