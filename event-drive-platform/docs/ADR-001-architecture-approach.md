# ADR-001: Архитектурный подход к event-driven платформе

**Статус:** Предложено  
**Дата:** 2026-11-06  
**Контекст:** Анализ требований `docs/eda-platform-requirements.md` и актуальных подходов 2025–2026

> **Уровень доказательств.** Веб-материал ниже получен из поисковой выдачи (выдержки), сами страницы не открывались и не сверялись с первоисточником, кроме тех, что уже сверены в разделе 7 требований ([О]). Блоги и вендорские статьи не являются независимыми замерами. Решение носит характер предложения, а не вывода из доказанных фактов. Разбивка по отдельным решениям: `memory/decisions/adr-001…008`.

---

## Контекст и проблема

Требуется платформа для обработки событий с тремя ключевыми характеристиками:

1. **Высокое быстродействие** — p99 latency в миллисекундах, пропускная способность до 110 000 событий/с на узле N3
2. **Высокая живучесть** — автономная работа узлов при сетевых ограничениях (T_aut от 3 с до 1 ч), горизонтальные связи при потере вертикали
3. **Распределённое развёртывание** — иерархия N0 (конечные устройства) → N1 (edge) → N2 (региональные) → N3 (ядро), cell-based изоляция отказов

Критичные события категории K (команды, модификации данных) не могут быть потеряны ни при каких условиях. События категории E (телеметрия, уведомления) допускают вытеснение по политике.

### Ключевые напряжения

Из анализа требований выявлены 9 конфликтов, которые нельзя снять одновременно:

1. **Долговечность vs задержка (P-3, P-5, R-3)** — fsync перед подтверждением увеличивает p99, но без него подтверждённые записи теряются при коррелированных отказах (Jepsen NATS 2.12.1: 679 153 потерянных из 1 367 069)
2. **Автономность vs безопасность (R-1, R-9, R-10)** — долгоживущие сертификаты покрывают изоляцию, но откладывают вступление отзыва прав
3. **Автономность vs согласованность (R-11)** — linearizable операции недоступны при разделении, только eventual/causal
4. **Порядок vs масштаб (P-7)** — строгий порядок в пределах ключа ограничивает параллелизм потребления
5. **Exactly-once vs границы системы (P-8)** — гарантия не распространяется на БД и внешние системы
6. **Ёмкость vs длительность изоляции (R-6, R-7, R-14)** — отказ приёма K допустим только после 96 ч при резерве на 48 ч × скорость K
7. **P2P-обмен vs долговечный журнал (R-2, R-3)** — peer-to-peer даёт горизонтальные связи, но не гарантирует durability
8. **Команды K и актуальность (R-17, R-18)** — команда с valid-until 48 ч может устареть при долгой изоляции
9. **Команды K на обеих сторонах разделения (R-17)** — single-writer обеспечивает порядок, но блокирует запись при недоступности владельца

---

## Обзор актуальных подходов (2025–2026)

### Долговечность и репликация

**Классическая репликация Kafka** (shared-nothing, ISR):
- **Плюсы**: зрелая экосистема, Apache 2.0, Kafka 4.0 (март 2025) полностью убрал ZooKeeper[^kafka-4], KRaft теперь единственный режим метаданных
- **Минусы**: `acks=all` по умолчанию не делает fsync перед подтверждением[^redpanda-fsync], тяжёл для edge-узлов, MirrorMaker 2 транслирует offsets с потерей точности (возможны дубли)[^kafka-vs-pulsar]
- **Замеры**: Jack Vanlightly (2023) показал деградацию Redpanda при высокой скорости fsync на мелких батчах[^vanlightly-kafka-redpanda]; Confluent заявил p99 3.5 с для Redpanda после 12 ч под 1 ГБ/с (конкурентный бенчмарк)[^edarch-2025]

**Redpanda** (Raft, C++):
- **Плюсы**: fsync каждого сообщения перед ack по умолчанию[^redpanda-prod-cfg], Kafka-совместимый API, без JVM, заявленный вендором выигрыш по tail latency ≥10× (в документе требований помечен [В])[^eda-2025-reqs]
- **Минусы**: BSL 1.1 с запретом предложения как сервиса третьим лицам[^eda-2025-reqs], enterprise-функции требуют ключ после 30-дневного trial, противоречивые результаты независимых замеров
- **Риск**: fsync можно отключить (`write.caching`), тогда гарантия теряется[^redpanda-prod-cfg]

**Apache Pulsar**:
- **Плюсы**: разделение compute (brokers) и storage (BookKeeper), нативная мульти-аренда, geo-replication, tiered storage, Apache 2.0[^kafka-vs-pulsar]
- **Минусы**: сложнее в эксплуатации (несколько компонентов), экосистема меньше Kafka[^edarch-2025]
- **Когда выбирать**: если нужна стабильная p99 latency при скачках нагрузки и tiered storage для долгого хранения[^kafka-vs-pulsar]

**NATS JetStream** (Raft, Go):
- **Плюсы**: лёгкий, Apache 2.0 (CNCF), leaf nodes для иерархии, pub/sub + streams в одной технологии[^nats-cncf]
- **Минусы**: Jepsen (декабрь 2025, версия 2.12.1) показал потерю подтверждённых записей при lazy fsync (flush раз в 2 мин)[^jepsen-nats], даже `--sync-interval always` не снял проблему целиком (5 из 5236 потеряны при смене состава кластера)[^jepsen-nats]; семантика mirror/source между доменами не проверена fault-injection тестами
- **Настройка**: `sync_interval: always` обязателен для K, проверять тестами (R-13)[^jepsen-nats]

**Object storage как основа** (AutoMQ, WarpStream):
- **Плюсы**: мульти-AZ репликация по умолчанию, атомарные PUT, операционно проще (меньше дисков)[^automq-payment]
- **Минусы**: латентность сотни мс — 1+ с (tiered storage), идемпотентные обработчики обязательны (дубли неизбежны)[^johal-object-storage]
- **Когда выбирать**: throughput-ориентированные потоки без жёстких SLO по latency[^johal-object-storage]

**Вывод по репликации**: для критичных K нужен fsync-before-ack + replication factor ≥3 + fault-domain spread[^jepsen-nats][^redpanda-fsync]. Kafka/NATS требуют явной настройки, Redpanda даёт по умолчанию.

### Автономность на краю (edge autonomy)

**Leaf nodes (NATS)**:
- Лист сам инициирует outbound-соединение к hub, обслуживает локальных клиентов и JetStream при потере связи[^nats-topologies]
- Streams и consumers размещаются в пределах одного кластера; механика сверки после восстановления не проверена fault-injection тестами[^eda-2025-reqs]

**Store-and-forward на краю**:
- Каждый узел фильтрует, агрегирует и обрабатывает данные локально, затем отправляет только агрегаты и алерты в облако[^avassa-edge] [^medium-edge-2026]
- Отложенная загрузка (только event logs, driving statistics) — типичный паттерн для автономных транспортных средств[^sciencedirect-edge]
- Патенты USPTO отмечают, что edge-узлы нужны для сетей с плохой связностью[^uspto-edge-resource]

**Kubernetes на краю**:
- KubeEdge (CNCF graduated, сент. 2024) заявляет edge autonomy[^kubeedge-graduation]; OCM klusterlet продолжает работать при падении hub, забирает ManifestWork pull-ом[^ocm-arch]
- Риск: не проверены под длительной изоляцией 5 мин — 1 ч и нагрузкой K × 100–11 000 событий/с[^eda-2025-reqs]

**Peer-to-peer mesh (Zenoh)**:
- EPL-2.0 OR Apache-2.0, peer-режим с multicast scouting и gossip, заявлено 16 µs peer-latency, 67 Gbps[^zenoh-overhead]
- Issue #2907 (открыт, метка «new feature»): peer, найденный через gossip, не переподключается автоматически после закрытия транспорта[^zenoh-issue-2907]; обход через client mode теряет shared-memory zero-copy
- Гарантии долговечности не проверены[^eda-2025-reqs]

**Вывод по автономности**: NATS leaf + JetStream domains покрывают иерархию одной технологией, но требуют явной настройки fsync и fault-injection проверки сверки после восстановления. Zenoh даёт P2P, но нужен отдельный durable-журнал для K.

### Изоляция отказов (fault isolation)

**Cell-based architecture** (AWS Well-Architected REL10-BP04):
- Каждая ячейка — полная независимая копия сервиса с фиксированным максимальным размером[^aws-cell-guidance]
- Partition key на входящем трафике выбирает ячейку; отказ остаётся внутри неё, остальные продолжают работу[^aws-cell-bulkhead]
- При 10 ячейках worst-case impact ≤10% клиентов; при 100 ячейках ≤1%[^appscale-cell-blast]
- Multi-AZ даёт fault tolerance, ячейки дают fault isolation от bad deployment, poison pill, tenant overload, operational mistake[^refonte-cell-2025]
- Shuffle sharding дополнительно снижает число клиентов в одном failure domain[^konishi-cell-shuffle]

**Trade-off**: крупные ячейки проще в эксплуатации и дешевле, но больший blast radius; мелкие — меньший blast radius, но выше операционная нагрузка без автоматизации[^aws-cell-guidance]

**Вывод по изоляции**: cell-based подход обязателен (D-3), выбор размера ячейки — по автоматизации и допустимому blast radius.

### Причинность и время

**Hybrid Logical Clock (HLC)** (Kulkarni, Demirbas 2014):
- Комбинирует физическое время с Lamport-счётчиками: `⟨l, c⟩`, где `l` — максимальное физическое время, `c` — счётчик[^rutgers-hlc][^javacodegeeks-hlc]
- Гарантия: если A → B, то HLC(A) < HLC(B); total order совместим с causality и примерно с физическим временем[^javacodegeeks-hlc]
- Используется в CockroachDB, YugabyteDB, MongoDB[^javacodegeeks-hlc][^medium-logical-time]
- Ограничение: HLC не доказывает concurrency (vector clocks могут, но растут неограниченно)[^rutgers-hlc]
- Расширения: Replay Clock (RepCl) для корректного replay логов, Hybrid Vector Clocks[^arxiv-replay-clocks][^arxiv-hybrid-vector]

**Вывод по времени**: HLC — баланс между causal порядком и физическим временем, подходит для R-5.

---

## Решение

### Архитектурный вариант: **Гибридный подход с двухслойной топологией**

**Ядро и регионы (N2–N3)**: Apache Kafka 4.x с KRaft
- **Причины**:
  - Зрелая экосистема, Apache 2.0, self-hosted без вендора (D-8)
  - KRaft убрал ZooKeeper (март 2025), упрощена эксплуатация[^kafka-4]
  - Tiered storage заявляется поисковой выдачей как поддерживаемый, но статус KIP-405 в документе требований не подтверждён [?], поэтому на него решение не опирается
  - Инструменты мониторинга, trace context (X-5, X-6), schema registry (X-2)
- **Настройки для K**:
  - `acks=all`, `min.insync.replicas=2` (при RF=3)
  - `flush.ms` и `flush.messages` по P-5: либо fsync-per-ack, либо явный flush каждые N мс с измеренным окном потерь и проверкой fault-injection тестами (R-13)
  - Проверить, достаточно ли батчинга и `linger.ms` для p99 ≤ 10 мс (P-2), иначе fallback на Redpanda для hot path
- **Репликация между регионами**: MirrorMaker 2 (KIP-1279 Cluster Mirroring статус Accepted, но пока требует Connect-воркеры[^kip-1279]); альтернатива — Confluent Cluster Linking (коммерческий) или дождаться KIP-1279 GA
- **Минусы**: MirrorMaker 2 транслирует offsets с возможными дублями, нужна идемпотентность (P-8)[^kafka-vs-pulsar]

**Edge-узлы (N1) и конечные устройства (N0)**: NATS JetStream
- **Причины**:
  - Лёгкий (Go), Apache 2.0 (CNCF), leaf nodes покрывают требование outbound-only (D-1)[^nats-cncf][^nats-topologies]
  - Иерархия leaf → hub с автономной работой JetStream в пределах T_aut (5 мин N1, 3 с N0)[^nats-jetstream-leaf]
  - Pub/sub + streams в одной технологии, проще для N0/N1 с ограниченными ресурсами
- **Обязательная настройка для K**:
  - `sync_interval: always` (R-3, R-15), проверить Jepsen-сценарий fault-injection (power loss, kill process, network partition, split-brain)[^jepsen-nats]
  - Replication factor = 3 для K, spread по fault domains (R-15)
  - Проверить семантику mirror/source между JetStream domains (R-4): либо поиск независимого отчёта, либо собственный fault-injection тест
- **Буфер N0**: 3 с × скорость (R-7), в памяти для E допустимо (решение заказчика), для K — либо энергонезависимая память, либо удержание отправителем до durable-ack следующего узла (R-3)
- **Минусы**: Jepsen NATS 2.12.1 показал потери даже с `--sync-interval always` при смене состава кластера (5 из 5236)[^jepsen-nats]; нужен собственный fault-injection CI (R-13)

**Мост N1 ↔ N2/N3**: NATS→Kafka connector (готовый компонент не подбирался, нужна оценка или разработка)
- Leaf N1 публикует K в локальный JetStream; connector переносит в Kafka N2/N3 с сохранением CloudEvents-обёртки (X-1) и идемпотентного ключа (P-8)
- Connector обеспечивает at-least-once, дедупликация по event ID в Kafka Streams или потребителях (P-8, R-4)

**Горизонтальные связи (R-2)**: кандидат NATS gateways (требует проверки)
- Гипотеза, не подтверждённая найденными источниками: NATS gateways соединяют кластеры, а не leaf-узлы, поэтому применимость к R-2 нужно проверить отдельно. Найденный материал её не подтверждает; задержку «сосед → сосед» без hub необходимо замерить

**Причинность**: HLC-метки (R-5, R-12)
- HLC в каждом событии: `⟨physical_time, counter⟩`, генерируется producer при создании события[^rutgers-hlc][^javacodegeeks-hlc]
- Идентификатор источника (node ID или producer ID)
- Глобальный total order не обещается, причинный порядок по HLC[^medium-logical-time]

**Cell-based развёртывание (D-3)**:
- Каждая ячейка — отдельный Kafka-кластер + NATS-leaf-узлы + connectors, без общего состояния[^aws-cell-guidance]
- Размер ячейки: ~1/20 клиентов → worst-case blast radius 5% (пороговое значение [П], уточнять нагрузочными тестами)
- Stateless маршрутизатор между ячейками (D-4), canary-деплой через ячейки волнами (D-5)[^refonte-cell-2025]

---

## Ключевые компромиссы

| Решение | Плюсы | Минусы | Остаточный риск |
|---------|-------|--------|-----------------|
| Kafka в ядре | Зрелость, экосистема, Apache 2.0, tiered storage | Тяжёл для edge, MirrorMaker 2 даёт дубли | Требует явной настройки flush для fsync[^redpanda-fsync] |
| NATS на краю | Лёгкий, leaf autonomy, outbound-only | Jepsen показал потери при lazy fsync и смене состава[^jepsen-nats] | Нужен собственный fault-injection CI (R-13) |
| HLC вместо vector clocks | Compact, близок к физическому времени | Не доказывает concurrency[^rutgers-hlc] | Допустимо для eventual consistency (R-11) |
| Single-writer для K (R-17) | Порядок применения команд сохранён | Модификация объекта блокируется при недоступности владельца | Команда ждёт в durable-очереди, статус «просрочена» через 48 ч (R-18) |
| Смешанный режим ack (R-15) | Подтверждение по локальному fsync без ожидания репликации | Полная потеря узла до репликации теряет K | Заказчик признал допустимым; алерт при lag > 30 мин |

---

## Последствия

### Позитивные
1. **Единая лицензия**: Apache 2.0 для Kafka и NATS, self-hosted без вендора (D-8)[^kafka-4][^nats-cncf]
2. **Проверяемость**: fault-injection CI с Jepsen-сценариями (R-13) покрывает power loss, split-brain, network partition[^jepsen-nats]
3. **Масштабируемость**: cell-based arch ограничивает blast radius до 5% (D-3)[^aws-cell-guidance]
4. **Observability**: CloudEvents + W3C traceparent + HLC дают сквозную трассировку (X-5, R-12)[^otel-messaging][^javacodegeeks-hlc]
5. **Эволюция**: Kafka 4.x KRaft упрощён без ZooKeeper, NATS лёгок для edge[^kafka-4][^nats-topologies]

### Негативные
1. **Две технологии**: нужен NATS-Kafka connector и единый контракт событий (X-1…X-3)
2. **Риск потерь K на NATS**: требует обязательной настройки `sync_interval: always` + fault-injection проверка (R-13)[^jepsen-nats]
3. **MirrorMaker 2 даёт дубли**: обработчики MUST быть идемпотентны по event ID (P-8)[^kafka-vs-pulsar]
4. **Операционная нагрузка**: две платформы требуют двух команд SRE, или сильной автоматизации (D-7, GitOps)
5. **Остаточный риск**: полная потеря узла до репликации теряет K (lag до 1 ч, R-15) — заказчик принял

### Требуется до принятия решения
1. Подтвердить заказчиком допустимость lag репликации K до 1 ч и остаточного риска потери при полной потере узла (R-15)
2. Проверить собственным fault-injection тестом: NATS JetStream с `sync_interval: always` + RF=3 + split-brain/power loss → 0 потерянных подтверждённых K (R-13)
3. Проверить семантику NATS mirror/source: восстановление после изоляции 5 мин (N1) даёт 0 потерянных K, 0 не-дедуплицированных дублей (R-4)
4. Замерить end-to-end p99 latency (producer → NATS → connector → Kafka → consumer) под устойчивой нагрузкой 100–11 000 событий/с, soak 12 ч: SLO p99 ≤ 10 мс для K (P-2, P-3)
5. Подтвердить пропускную способность каналов N2 ↔ N2 (~55 ГБ/с) и N3 ↔ N3 (~100 ГБ/с) для догонки репликации K за 2 ч после изоляции 48 ч (R-8), а также что дисковая и сетевая подсистема узла выдерживает такой приём поверх собственной нагрузки (в документе требований это не анализируется; 100 ГБ/с — около 800 Гбит/с на узел)
6. Выбор брокера для N2–N3 не подтверждён измерениями на нагрузке 110 000 событий/с и 2 ГБ/с: решение в этой части остаётся гипотезой до soak-теста (P-3)

---

## Альтернативы рассмотрены

### A. NATS-центричный (leaf + JetStream domains + gateways по всей иерархии)
- **Отклонено**: Kafka в ядре опирается на зрелость экосистемы и широкий операционный опыт (оценка по обзорным источникам[^kafka-vs-pulsar], не по замерам); пригодность NATS для долгого хранения K на 48 ч при 2 ГБ/с в найденных источниках не оценивалась

### B. Kafka везде (ядро + edge через MM2)
- **Отклонено**: Kafka тяжёл для N0/N1 (JVM, ZooKeeper — теперь KRaft, но всё равно heavy для embedded), не даёт outbound-only leaf autonomy из коробки (D-1), MirrorMaker 2 на каждом edge-узле — операционно сложно[^eda-2025-reqs]

### C. Pulsar
- **Отклонено**: сложнее в эксплуатации (BookKeeper + brokers), меньше экосистемы, выигрыш в multi-tenancy и tiered storage не критичен для данной задачи (все узлы — внутренние, один тенант)[^edarch-2025]

### D. Redpanda везде
- **Отклонено**: BSL 1.1 запрещает предложение как сервиса третьим лицам (D-8), enterprise-функции под ключом, противоречивые бенчмарки[^eda-2025-reqs][^vanlightly-kafka-redpanda]; вариант оставить Redpanda для N2/N3 hot path, если Kafka не пройдёт p99 ≤ 10 мс

### E. Zenoh P2P + durable журнал
- **Отклонено**: issue #2907 (peer не переподключается автоматически), гарантии долговечности не проверены[^zenoh-issue-2907]; оставить как исследовательский трек для горизонтальных связей (R-2), если NATS gateways не покажут нужной задержки

---

## Источники

[^kafka-4]: [Wikipedia: Apache Kafka](https://en.wikipedia.org/wiki/Apache_Kafka)  
[^redpanda-fsync]: [Redpanda Blog: Why fsync() is needed for data safety](https://www.redpanda.com/blog/why-fsync-is-needed-for-data-safety-in-kafka-or-non-byzantine-protocols)  
[^kafka-vs-pulsar]: [Java Code Geeks: Event-Driven Architecture: Kafka vs. RabbitMQ vs. Pulsar - A 2025 Decision Framework](https://www.javacodegeeks.com/2025/12/event-driven-architecture-kafka-vs-rabbitmq-vs-pulsar-a-2025-decision-framework.html)  
[^vanlightly-kafka-redpanda]: [Jack Vanlightly: Kafka vs Redpanda Performance - Do the claims add up?](https://jack-vanlightly.com/blog/2023/5/15/kafka-vs-redpanda-performance-do-the-claims-add-up)  
[^edarch-2025]: [Growin: Event Driven Architecture Done Right: How to Scale Systems with Quality in 2025](https://www.growin.com/blog/event-driven-architecture-scale-systems-2025/)  
[^eda-2025-reqs]: `docs/eda-platform-requirements.md`, раздел 6 «Кандидаты технологий и лицензии»  
[^redpanda-prod-cfg]: [Redpanda Docs: Configure Producers](https://docs.redpanda.com/cloud-data-platform/develop/produce-data/configure-producers/)  
[^automq-payment]: [AutoMQ Blog: Payment Event Streaming: Reliability Patterns for Financial Services](https://www.automq.com/blog/payment-event-streaming-reliability-patterns-financial-services)  
[^johal-object-storage]: [Johal.in: Durable Event Streams on Object Storage](https://johal.in/object-storage-durable-streams-guide)  
[^jepsen-nats]: [Jepsen: NATS 2.12.1](https://jepsen.io/analyses/nats-2.12.1)  
[^nats-cncf]: [CNCF Blog: Protecting NATS and the Integrity of Open Source](https://www.cncf.io/blog/2025/05/01/protecting-nats-and-the-integrity-of-open-source-cncfs-commitment-to-the-community/)  
[^nats-topologies]: [NATS Docs: Topologies](https://docs.nats.io/concepts/topologies)  
[^nats-jetstream-leaf]: [NATS Docs: JetStream on Leaf Nodes](https://docs.nats.io/running-a-nats-service/configuration/leafnodes/jetstream_leafnodes)  
[^kip-1279]: [Kafka Wiki: KIP-1279 Cluster Mirroring](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1279:+Cluster+Mirroring)  
[^avassa-edge]: [Avassa: Industrial Edge Computing: Scaling Smart Factory Operations in 2026](https://avassa.io/articles/smart-factories-edge-computing-manufacturing/)  
[^medium-edge-2026]: [Medium: What Is Edge Computing in 2026?](https://medium.com/@neovise/what-is-edge-computing-in-2026-how-it-works-and-its-types-ff10ba01d0ab)  
[^sciencedirect-edge]: [ScienceDirect: Driving the future with edge computing (abstract)](https://www.sciencedirect.com/science/article/abs/pii/S2542660526000934)  
[^uspto-edge-resource]: USPTO patent 10958583: Edge-node controlled resource distribution  
[^kubeedge-graduation]: [CNCF: KubeEdge Graduation](https://www.cncf.io/announcements/2024/10/15/cloud-native-computing-foundation-announces-kubeedge-graduation/)  
[^ocm-arch]: [Open Cluster Management: Architecture](https://open-cluster-management.io/docs/concepts/architecture/)  
[^zenoh-overhead]: [Zenoh Blog: Zenoh Overhead](https://zenoh.io/blog/2021-07-05-zenoh-overhead/)  
[^zenoh-issue-2907]: [Zenoh GitHub issue #2907](https://github.com/eclipse-zenoh/zenoh/issues/2907)  
[^aws-cell-guidance]: [AWS GitHub: Guidance for Cell-Based Architecture on AWS](https://github.com/aws-solutions-library-samples/guidance-for-cell-based-architecture-on-aws)  
[^aws-cell-bulkhead]: [AWS Well-Architected: REL10-BP04 Use bulkhead architectures](https://docs.aws.amazon.com/en_us/wellarchitected/2022-03-31/framework/rel_fault_isolation_use_bulkhead.html)  
[^appscale-cell-blast]: [AppScale Blog: Cell-Based Architecture: Blast Radius by Design](https://appscale.blog/en/blog/cell-based-architecture-blast-radius-shuffle-sharding-cell-routing-2026)  
[^refonte-cell-2025]: [Refonte Learning: Cell-Based Architecture: The Lesson From 2025's Outages](https://www.refontelearning.com/blog/cell-based-architecture-cloud-outage-resilience)  
[^konishi-cell-shuffle]: [Hidekazu Konishi: Cell-Based Architecture and Shuffle Sharding on AWS](https://hidekazu-konishi.com/entry/cell_based_architecture_and_shuffle_sharding_on_aws.html)  
[^rutgers-hlc]: [Rutgers CS 417 notes: Hybrid Logical Clocks (PDF)](https://people.cs.rutgers.edu/~pxk/assets/files/classes-417-notes/03r-HLC.pdf)  
[^javacodegeeks-hlc]: [Java Code Geeks: Decoding Distributed Time: Vector Clocks vs. Hybrid Logical Clocks](https://www.javacodegeeks.com/2026/08/decoding-distributed-time-vector-clocks-vs-hybrid-logical-clocks.html)  
[^medium-logical-time]: [Medium: Distributed systems: Logical Time Explained](https://medium.com/@armironenko/distributed-systems-logical-time-explained-5f97949f180f)  
[^arxiv-replay-clocks]: [arXiv 2407.00069: Tracing Distributed Algorithms Using Replay Clocks](https://arxiv.org/pdf/2407.00069)  
[^arxiv-hybrid-vector]: [arXiv 2311.07535: Causality Diagrams using Hybrid Vector Clocks](https://arxiv.org/pdf/2311.07535)  
[^otel-messaging]: [OpenTelemetry: Messaging Spans](https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/)
