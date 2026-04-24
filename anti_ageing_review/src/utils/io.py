from __future__ import annotations
from pathlib import Path
from datetime import datetime
import yaml
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

def load_config(path='config/review_config.yaml'):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    cfg = yaml.safe_load(p.read_text(encoding='utf-8'))
    cfg['_root'] = ROOT
    for key, val in cfg.get('paths', {}).items():
        out = ROOT / val
        out.mkdir(parents=True, exist_ok=True)
        cfg['paths'][key] = out
    return cfg

def save_csv(df, path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False)

def append_log(path, phase, completed, outputs, remaining, risks, next_command):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    block = f'''
---
## {phase}
Date/time: {stamp}

Completed:
{completed}

Outputs created:
{outputs}

Remaining tasks:
{remaining}

Risks/limitations:
{risks}

Exact next command:
`{next_command}`
'''
    with p.open('a', encoding='utf-8') as f:
        f.write(block)

def now_iso():
    return datetime.now().isoformat(timespec='seconds')
