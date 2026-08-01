---
type: insight
id: comparative-alignment-2026
title: "Сравнительный анализ (1/2): где современные подходы 2026 года совпадают с кайдзен по сути, а не по названию"
recorded_at: '2026-08-01T20:00:00Z'
summary: >-
  Синтез insight-записей Этапов 1-3 без новых источников. Общий паттерн:
  практически все рассмотренные тенденции 2026 года по структуре
  воспроизводят один из двух базовых циклов кайдзен — PDCA (улучшение через
  итерацию) или SDCA (стандартизация перед улучшением) — либо принцип gemba
  (решения на основе проверенного факта, а не отчёта/представления), но без
  использования кайдзен-терминологии. (1) PDCA-паттерн: Agile-итерация
  сглаживает кривую стоимости изменений через короткий цикл обратной связи
  ([[memory/insights/cost-of-change-2026]]); fitness functions в эволюционной
  архитектуре — автоматизированный PDCA/SDCA на уровне архитектуры
  ([[memory/insights/evolutionary-architecture-2026]]); SRE кодифицирует
  SLO как стандарт и error budget как механизм Act
  ([[memory/insights/sre-devops-2026]]); METR-исследование само по себе —
  пример необходимости повторной проверки (Check) единичного измерения
  ([[memory/insights/ai-assisted-development-2026]]). (2) SDCA-паттерн:
  platform engineering стандартизирует повторяющиеся операции прежде, чем
  команды начинают их улучшать ([[memory/insights/platform-engineering-2026]]).
  (3) Gemba-паттерн: continuous discovery — еженедельный контакт с клиентом
  вместо разового сбора требований, прямой ответ на разрыв бизнес-требований
  ([[memory/insights/continuous-discovery-2026]],
  [[memory/insights/requirements-gap-2026]]); Amazon single-threaded leader —
  подотчётный лидер обязан быть "у места создания ценности"
  ([[memory/insights/amazon-2026]]); Spotify пересмотрел собственную модель
  через цикл Check/Act, когда гемба показала её неполноту
  ([[memory/insights/spotify-2026]]).
entities: [kaizen, pdca, sdca, gemba, cost-of-change, evolutionary-architecture, sre, platform-engineering, continuous-discovery, requirements-gap, amazon, spotify, team-topologies, ai-assisted-development]
sources:
- memory/insights/cost-of-change-2026.md
- memory/insights/evolutionary-architecture-2026.md
- memory/insights/sre-devops-2026.md
- memory/insights/ai-assisted-development-2026.md
- memory/insights/platform-engineering-2026.md
- memory/insights/continuous-discovery-2026.md
- memory/insights/requirements-gap-2026.md
- memory/insights/amazon-2026.md
- memory/insights/spotify-2026.md
confidence: medium
---

Дополнительная ценность кайдзен-рамки поверх найденных совпадений: тройка
muda/mura/muri ([[memory/facts/muda/definition]],
[[memory/facts/mura/definition]], [[memory/facts/muri/definition]]) даёт
более гранулярный диагностический язык, чем единая метрика "технический
долг" ([[memory/insights/technical-debt-2026]]) или "trust/friction" в
DORA 2025 ([[memory/insights/dora-metrics-2026]]): она разделяет потери на
явно устранимые (muda), неравномерность потока (mura) и перегрузку
(muri) — три разных диагноза, требующих разных вмешательств, тогда как
современные отчёты (McKinsey, DORA, Faros AI) чаще смешивают их в одном
показателе. Явное разделение SDCA (сначала стандарт) → PDCA (потом
улучшение) также напрямую адресует проблему platform engineering — 29.6%
платформенных команд не измеряют результат
([[memory/insights/platform-engineering-2026]]) именно потому, что
пропускают Standardize/Check-фазу и переходят к "улучшению" без
зафиксированного и проверяемого стандарта.
