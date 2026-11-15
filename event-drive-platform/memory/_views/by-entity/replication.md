# Facts — replication

- **catchup-by-isolation**: I≤6 ч: 2 ч; I=24 ч: 8 ч; I=48 ч: 16 ч при C=4r (unknown → present) — `memory/facts/replication/catchup-by-isolation.md`
- **replication-catchup-limit**: 2 h при изоляции до 6 ч; 8 h при 24 ч; 16 h при 48 ч (при канале 4r) (unknown → present) — `memory/facts/replication/replication-catchup-limit.md`
- **replication-catchup-requirement**: C ≥ 4r для догонки 2 h при изоляции 6 ч; C ≥ 13r при 24 ч; C ≥ 25r при 48 ч (unknown → present) — `memory/facts/replication/replication-catchup-requirement.md`
- **replication-factor**: ×3 (две копии на соседних узлах того же класса) (2026-11-06 → present) — `memory/facts/replication/replication-factor.md`
- **replication-lag-limit**: 1 h при работающей связи, алерт на 30 мин (2026-11-06 → present) — `memory/facts/replication/replication-lag-limit.md`
