# Internal Peer Review 1 - Epidemiology and Causal Interpretation

## Overall Recommendation

Revise before submission. The research question is relevant for geriatric public health in India, but the manuscript must avoid presenting ecological state-level results as individual-level ageing prediction.

## Major Comments

1. **Ecological design must be explicit throughout.**  
   The LASI real-data analysis uses state/UT summaries. It cannot estimate individual frailty risk, individual biological ageing, or causal exposure effects.

2. **Mortality result should be described as supportive, not confirmatory.**  
   The association between DEAI and old-age death rate is stable after excluding the India row (rho=+0.341, p=0.042), but FDR q=0.146 after seven outcome tests. It should be framed as nominal and hypothesis-supporting.

3. **Multimorbidity inverse association is real but needs transition framing.**  
   The robust inverse association (rho=-0.777, FDR q<0.001) should not be interpreted as a protective effect. The most plausible explanation is epidemiological transition, survival selection, and differential diagnosis/ascertainment.

4. **India national row should not be treated as an independent state.**  
   Primary sensitivity results should exclude the national India row. Including it is acceptable only as a descriptive comparison.

5. **Claims about biological ageing need careful qualification.**  
   The manuscript can describe DEAI as an upstream exposome-risk index and ecological healthy-ageing surveillance tool. It should not claim direct biological-age measurement without molecular or individual-level validation.

## Minor Comments

- Add bootstrap confidence intervals for key ecological correlations.
- Report leave-one-out influence checks.
- Report internal consistency of the multi-domain DEAI components.
- Include a clear limitation about health-system ascertainment bias in diagnosed chronic disease.

## Author Response / Changes Made

- Added states-only robustness analysis excluding the India row.
- Added bootstrap 95% intervals, leave-one-out ranges, and FDR q-values.
- Revised mortality language to "stable nominal/supportive."
- Added epidemiological transition paradox interpretation to the abstract, results, discussion, and real-data annex.
- Added explicit ecological-inference limitations.
- Added component reliability summary: Cronbach alpha=0.688.
