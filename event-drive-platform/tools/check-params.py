#!/usr/bin/env python3
"""Check that ids referenced in docs exist in docs/parameters.yaml, no duplicates,
and that derived values match their formulas."""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PARAMS = ROOT / "docs/parameters.yaml"
DOCS = [ROOT / "docs/adr", ROOT / "docs/eda-platform-requirements.md"]

ID_RE = re.compile(r"`([A-Z]-[A-Z0-9]+(?:-[A-Z0-9]+)*)`")

TOLERANCE = {"events": 0.5, "events/s": 0.5, "KB": 0.5, "h": 0.5}


def load_params():
    data = yaml.safe_load(PARAMS.read_text(encoding="utf-8"))
    params, dupes = {}, []
    for section, items in data.items():
        if section == "meta":
            continue
        for pid, body in items.items():
            if pid in params:
                dupes.append(pid)
            params[pid] = body
    return params, dupes


def derived(params):
    """Return {id: computed value}. Volume is K only; reserve and physical add
    expiry records, matching the tables in the requirements document."""
    p = {k: v["value"] for k, v in params.items()}
    out = {}

    def need(*ids):
        return all(i in p for i in ids)

    if need("L-N2-K-RATE", "L-N2-SUBORDINATES", "L-N1-K-RATE"):
        out["L-N2-K-RATE-FULL"] = p["L-N2-K-RATE"] + p["L-N2-SUBORDINATES"] * p["L-N1-K-RATE"]
    if need("L-N2-K-VOL", "L-N2-SUBORDINATES", "L-N1-K-VOL"):
        mb = p["L-N2-K-VOL"] + p["L-N2-SUBORDINATES"] * p["L-N1-K-VOL"]
        out["L-N2-K-VOL-FULL"] = round(mb / 1000, 3)
    if need("L-N3-K-RATE", "L-N3-SUBORDINATES", "L-N2-K-RATE"):
        out["L-N3-K-RATE-FULL"] = p["L-N3-K-RATE"] + p["L-N3-SUBORDINATES"] * p["L-N2-K-RATE"]
    if need("L-N3-K-VOL", "L-N3-SUBORDINATES", "L-N2-K-VOL"):
        mb = p["L-N3-K-VOL"] * 1000 + p["L-N3-SUBORDINATES"] * p["L-N2-K-VOL"]
        out["L-N3-K-VOL-FULL"] = round(mb / 1000, 3)

    if not need("D-K-RETENTION", "D-EXPIRY-RECORD-SIZE", "D-REPLICA-COUNT", "D-MIRROR-COUNT"):
        return out
    hours = p["D-K-RETENTION"]
    secs = hours * 3600
    for name, vol, rate, unit_div in (("N1", "L-N1-K-VOL", "L-N1-K-RATE", 1e6),
                                      ("N2", "L-N2-K-VOL-FULL", "L-N2-K-RATE-FULL", 1e3),
                                      ("N3", "L-N3-K-VOL-FULL", "L-N3-K-RATE-FULL", 1e3)):
        if not need(vol, rate):
            continue
        volume = round(p[vol] * secs / unit_div, 2)                     # TB, K only
        record = p[rate] * p["D-EXPIRY-RECORD-SIZE"] * secs / 1e12     # TB
        total = volume + record
        out[f"D-K-VOLUME-{name}"] = volume
        out[f"D-K-RESERVE-{name}"] = round(total * p["D-REPLICA-COUNT"], 1)
        out[f"D-K-PHYSICAL-{name}"] = round(total * p["D-REPLICA-COUNT"] * p["D-MIRROR-COUNT"], 1)
    return out


def doc_files():
    files = [DOCS[1]] if DOCS[1].exists() else []
    for d in DOCS[:1]:
        files += sorted(d.rglob("*.md"))
    return [f for f in files if f.exists()]


def main():
    params, dupes = load_params()
    errors = [f"duplicate parameter id: {d}" for d in dupes]

    for f in doc_files():
        text = f.read_text(encoding="utf-8")
        for pid in set(ID_RE.findall(text)):
            if pid not in params:
                errors.append(f"{f.relative_to(ROOT)}: unknown parameter id {pid}")

    for pid, value in derived(params).items():
        if pid not in params:
            errors.append(f"derived value {pid} missing from parameters.yaml")
            continue
        declared = params[pid]["value"]
        unit = params[pid].get("unit")
        tol = TOLERANCE.get(unit, max(abs(declared) * 0.005, 0.05))
        if abs(declared - value) > tol:
            errors.append(f"{pid}: declared {declared} but formula gives {round(value, 2)} ({unit})")

    for e in errors:
        print(f"ERROR: {e}")
    if not errors:
        print(f"params ok ({len(params)} ids, {len(doc_files())} docs)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
