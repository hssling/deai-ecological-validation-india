"""Shared utilities: config loading, path resolution, structured logging, amendment log."""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


def load_config(path: str | Path) -> dict:
    cfg_path = Path(path).resolve()
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    project_root = cfg_path.parents[1]
    for k, v in cfg["paths"].items():
        raw = Path(v)
        if raw.is_absolute():
            resolved = raw
        else:
            parts = raw.parts
            if project_root.name in parts:
                idx = parts.index(project_root.name)
                suffix = Path(*parts[idx + 1:]) if idx + 1 < len(parts) else Path()
                resolved = project_root / suffix
            elif raw.exists():
                resolved = raw
            else:
                resolved = project_root / raw
        cfg["paths"][k] = resolved
    return cfg


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str, **fields) -> None:
    payload = {"t": now_iso(), "msg": msg, **fields}
    print(json.dumps(payload, default=str), flush=True)


def ensure_dirs(*paths) -> None:
    for p in paths:
        Path(p).mkdir(parents=True, exist_ok=True)


def append_amendment(docs_dir, what: str, why: str) -> None:
    f = Path(docs_dir) / "amendment_log.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(f"\n## {now_iso()}\n- **What:** {what}\n- **Why:** {why}\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--config", default="config/meta_config.yaml")
    a = ap.parse_args()
    if a.check:
        cfg = load_config(a.config)
        for v in cfg["paths"].values():
            ensure_dirs(v)
        log("scaffold_ok", paths=list(cfg["paths"].keys()))
        sys.exit(0)
