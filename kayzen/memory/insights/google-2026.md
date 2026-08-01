---
type: insight
id: google-2026
title: "Google SRE: происхождение практики и неподтверждённая прямая связь с DORA"
recorded_at: '2026-08-01T19:08:00Z'
summary: >-
  Site Reliability Engineering возникла в Google в 2003 году, термин ввёл
  Ben Treynor Sloss; к 2016 году в Google было 1000+ инженеров на
  SRE-позициях. Фундаментальная книга "Site Reliability Engineering: How
  Google Runs Production Systems" (2017) — сборник эссе сотрудников Google
  SRE (разделы Introduction/Principles/Practices/Management), за ней
  последовали "The Site Reliability Workbook" и "Building Secure and
  Reliable Systems". Практика распространилась в индустрии широко за
  пределами Google (Airbnb, Dropbox, IBM, LinkedIn, Netflix, Wikimedia;
  ~22% adoption по опросу DevOps Institute 2021). Веб-поиск не нашёл
  первичного источника, прямо связывающего команду Google SRE с созданием
  DORA-метрик ([[memory/insights/dora-metrics-2026]]): связь Google с DORA
  носит организационный характер (приобретение DORA компанией Google Cloud
  в 2018 году), а не методологический — DORA-метрики разработаны Nicole
  Forsgren, Jez Humble и Gene Kim независимо от практики SRE.
entities: [google, sre, dora-metrics]
sources:
- memory/sources/google-2026.md
confidence: medium
---

Связь с кайдзен: SRE формализует роль, ответственную за непрерывный поиск
и устранение источников нестабильности (error budgets, postmortems без
поиска виновных) — это структурно близко к PDCA
([[memory/facts/pdca/definition]]) в применении к операционной надёжности,
и к принципу "стандартизировать, затем улучшать" (SDCA,
[[memory/facts/sdca/definition]]): SLO/error budget — это стандарт, а
postmortem-цикл — механизм Act. Важно для Этапа 4: часто в популярных
пересказах Google SRE и DORA сливаются в единый "Google-бренд" передовой
инженерной культуры — этот вывод следует явно разъединить в итоговом
документе, так как это два разных источника происхождения (внутренняя
практика Google vs приобретённая исследовательская команда), объединённые
только фактом владения, а не общей методологией. Не сглаживать этот разрыв
в документе Видение — отмечено явно, как того требует
`memory/projects/kaizen-swdev-methodology.md` (раздел "Открытые вопросы").
