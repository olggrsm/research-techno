---
type: transaction
transaction_id: txn-k-split-catchup-trevoke--20261115t114106z-f12eaae4
idempotency_key: k-split-catchup-trevoke-2026-11-15
agent_id: agent-agent-claude-code-336829bb
created_at: '2026-11-15T11:41:06.874299Z'
status: committed
expected_revision: null
committed_revision: c149952d23a0e537e271932b05d8e45d61e226c4
failure_reason: null
committed_at: '2026-11-15T11:43:18.435796Z'
ops:
- op: update_fact
  entity: replication
  predicate: replication-catchup-limit
  value: 2 h при изоляции до 6 ч; 8 h при 24 ч; 16 h при 48 ч (при канале 4r)
  target_path: memory/facts/replication/replication-catchup-limit.md
  precondition_hash: sha256:e58183569373f6ebc69380657c6f4967d6678fbcff3d017c7d1d340004f97860
- op: update_fact
  entity: replication
  predicate: replication-catchup-requirement
  value: C ≥ 4r для догонки 2 h при изоляции 6 ч; C ≥ 13r при 24 ч; C ≥ 25r при 48
    ч
  target_path: memory/facts/replication/replication-catchup-requirement.md
  precondition_hash: sha256:05d57e9bad3ada9025c7b1361bff989bd5c076612edaf4955d6f20e6293cf771
- op: create_fact
  entity: k-command
  predicate: k-command-rate
  value: 10/с (N1), 1 000/с (N2), 10 000/с (N3)
  target_path: memory/facts/k-command/k-command-rate.md
- op: create_fact
  entity: k-fact
  predicate: k-fact-rate
  value: 90/с (N1), 10 000/с (N2), 100 000/с (N3)
  target_path: memory/facts/k-fact/k-fact-rate.md
- op: create_fact
  entity: k-command
  predicate: k-command-fact-ratio
  value: 1:10 (команды к фактам), применено к скорости и объёму
  target_path: memory/facts/k-command/k-command-fact-ratio.md
- op: create_fact
  entity: platform
  predicate: k-namespace-scheme
  value: k.cmd.<region>.<domain>.<verb>.<object>; k.fact.<region>.<domain>.<object>.<event>;
    e.<region>.<domain>.<stream>
  target_path: memory/facts/platform/k-namespace-scheme.md
- op: create_fact
  entity: platform
  predicate: command-p99-local
  value: 20 мс
  target_path: memory/facts/platform/command-p99-local.md
- op: create_fact
  entity: platform
  predicate: command-p99-peer
  value: 200 мс
  target_path: memory/facts/platform/command-p99-peer.md
- op: create_fact
  entity: platform
  predicate: fact-p99-local
  value: 50 мс
  target_path: memory/facts/platform/fact-p99-local.md
- op: create_fact
  entity: platform
  predicate: bulk-p99
  value: 1 с
  target_path: memory/facts/platform/bulk-p99.md
- op: create_fact
  entity: platform
  predicate: t-revoke
  value: 15 мин
  target_path: memory/facts/platform/t-revoke.md
- op: create_fact
  entity: k-command
  predicate: expiry-record-ttl
  value: 10 h
  target_path: memory/facts/k-command/expiry-record-ttl.md
- op: create_fact
  entity: k-fact
  predicate: dedup-ttl-k
  value: 7 суток
  target_path: memory/facts/k-fact/dedup-ttl-k.md
- op: create_fact
  entity: platform
  predicate: dedup-ttl-e
  value: 3 суток
  target_path: memory/facts/platform/dedup-ttl-e.md
- op: create_fact
  entity: node-n0
  predicate: n0-role
  value: 'датчик или исполнитель без диска: хранит только E (буфер 3 с в памяти),
    K не порождает, получает K-команду от N1'
  target_path: memory/facts/node-n0/n0-role.md
- op: create_fact
  entity: replication
  predicate: catchup-by-isolation
  value: 'I≤6 ч: 2 ч; I=24 ч: 8 ч; I=48 ч: 16 ч при C=4r'
  target_path: memory/facts/replication/catchup-by-isolation.md
---

# Transaction: txn-k-split-catchup-trevoke--20261115t114106z-f12eaae4

Status: **committed**

Applied 16 operation(s) atomically.

Idempotency key `k-split-catchup-trevoke-2026-11-15` — replaying this key is a no-op while this journal exists.
