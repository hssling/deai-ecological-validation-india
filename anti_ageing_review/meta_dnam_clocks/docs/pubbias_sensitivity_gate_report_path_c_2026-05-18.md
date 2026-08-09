# Publication Bias & Sensitivity Gate Report — Path-C

Generated: 2026-05-18

## Gates

- Egger / Begg / PET-PEESE require k>=`10`; gate-failed here.
- Leave-one-out runs at k>=`3`.
- Low-RoB-only requires dual-coded RoB2 (currently all `pending`).
- Duration>=12-week sensitivity runs when `duration_weeks` is extracted.

## Summary rows

| Clock | Analysis | k | μ | 95% CI | Status |
|---|---|---|---|---|---|
| DunedinPACE | publication_bias_egger | 3 | — | — | gate_failed |
| DunedinPACE | publication_bias_begg | 3 | — | — | gate_failed |
| DunedinPACE | pet_peese | 3 | — | — | gate_failed |
| DunedinPACE | leave_one_out:drop=ChapnickM_2025_d1605d | 2 | 0.0830 | [-0.288, 0.454] | performed |
| DunedinPACE | leave_one_out:drop=CorleyMJ_2025_ad19fa | 2 | 0.1079 | [-0.203, 0.418] | performed |
| DunedinPACE | leave_one_out:drop=MerrillSM_2024_5ee99d | 2 | -0.0495 | [-0.105, 0.006] | performed |
| DunedinPACE | restrict_low_rob | 3 | — | — | gate_failed_pending_rob |
| DunedinPACE | restrict_duration_ge_12wk | 0 | — | — | gate_failed |
| GrimAge | publication_bias_egger | 2 | — | — | gate_failed |
| GrimAge | publication_bias_begg | 2 | — | — | gate_failed |
| GrimAge | pet_peese | 2 | — | — | gate_failed |
| GrimAge2 | publication_bias_egger | 1 | — | — | gate_failed |
| GrimAge2 | publication_bias_begg | 1 | — | — | gate_failed |
| GrimAge2 | pet_peese | 1 | — | — | gate_failed |
| PCClock | publication_bias_egger | 1 | — | — | gate_failed |
| PCClock | publication_bias_begg | 1 | — | — | gate_failed |
| PCClock | pet_peese | 1 | — | — | gate_failed |
| PhenoAge | publication_bias_egger | 1 | — | — | gate_failed |
| PhenoAge | publication_bias_begg | 1 | — | — | gate_failed |
| PhenoAge | pet_peese | 1 | — | — | gate_failed |

## Honest interpretation

- Publication-bias diagnostics are uninformative at k=3 and are correctly gate-failed.
- Leave-one-out shows whether any single study drives the pooled DunedinPACE estimate.
- Low-RoB-only sensitivity will remain `gate_failed_pending_rob` until dual coding is completed.