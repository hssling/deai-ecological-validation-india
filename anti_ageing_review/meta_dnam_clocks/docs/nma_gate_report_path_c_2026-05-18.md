# Network Meta-Analysis Gate Report — Path-C

Generated: 2026-05-18

## Gate

- Required: k>=`10` per clock with a connected network.
- Current state: every clock has k<10. NMA is NOT performed.

## Per-clock

| Clock | k | NMA performed | Reason |
|---|---|---|---|
| DunedinPACE | 3 | no | k=3 < 10; below NMA threshold |
| GrimAge | 2 | no | k=2 < 10; below NMA threshold |
| GrimAge2 | 1 | no | k=1 < 10; below NMA threshold |
| PhenoAge | 1 | no | k=1 < 10; below NMA threshold |
| Horvath | 0 | no | k=0 < 10; below NMA threshold |
| Hannum | 0 | no | k=0 < 10; below NMA threshold |
| PCClock | 1 | no | k=1 < 10; below NMA threshold |
| DNAmTL | 0 | no | k=0 < 10; below NMA threshold |

## Honest interpretation

- Even for DunedinPACE (k=3), an NMA would be uninformative and risk false precision.
- We therefore present pairwise random-effects pooling only.