#!/usr/bin/env Rscript
# R cross-check pool for the DNAm clocks meta-analysis (A3 amendment).
# Inputs : a CSV with columns study_id, value, se
# Outputs: a JSON with DL, HKSJ, and Bayesian (bayesmeta) pooled estimates.
suppressPackageStartupMessages({
  library(meta)
  library(bayesmeta)
  library(jsonlite)
})

args <- commandArgs(trailingOnly = TRUE)
get_arg <- function(flag) {
  i <- which(args == flag)
  if (length(i) == 0) stop(paste("missing", flag))
  args[i + 1]
}
in_csv  <- get_arg("--input")
out_json <- get_arg("--output")

df <- read.csv(in_csv, stringsAsFactors = FALSE)
stopifnot(all(c("study_id","value","se") %in% names(df)))
df <- df[!is.na(df$value) & !is.na(df$se) & df$se > 0, ]

# DerSimonian-Laird random-effects
m_dl <- metagen(TE = df$value, seTE = df$se, studlab = df$study_id,
                sm = "MD", method.tau = "DL", prediction = TRUE,
                random = TRUE, common = FALSE)

# HKSJ random-effects (use HK adjustment for CIs)
m_hk <- metagen(TE = df$value, seTE = df$se, studlab = df$study_id,
                sm = "MD", method.tau = "DL", random = TRUE, common = FALSE,
                method.random.ci = "HK")

# Bayesian meta (half-normal(0, 0.5) prior on tau)
bm <- tryCatch(
  bayesmeta(y = df$value, sigma = df$se, labels = df$study_id,
            tau.prior = function(t) dhalfnormal(t, scale = 0.5),
            interval.type = "central"),
  error = function(e) NULL
)

out <- list(
  k = nrow(df),
  r_dl_mu        = unname(m_dl$TE.random),
  r_dl_ci_lower  = unname(m_dl$lower.random),
  r_dl_ci_upper  = unname(m_dl$upper.random),
  r_dl_pi_lower  = unname(m_dl$lower.predict),
  r_dl_pi_upper  = unname(m_dl$upper.predict),
  r_dl_tau2      = unname(m_dl$tau2),
  r_dl_I2        = unname(m_dl$I2),
  r_hksj_mu       = unname(m_hk$TE.random),
  r_hksj_ci_lower = unname(m_hk$lower.random),
  r_hksj_ci_upper = unname(m_hk$upper.random)
)

if (!is.null(bm)) {
  s <- summary(bm)
  out$r_bayes_mu_median <- unname(bm$summary["median", "mu"])
  out$r_bayes_ci_lower  <- unname(bm$summary["95% lower", "mu"])
  out$r_bayes_ci_upper  <- unname(bm$summary["95% upper", "mu"])
} else {
  out$r_bayes_mu_median <- NA_real_
  out$r_bayes_ci_lower  <- NA_real_
  out$r_bayes_ci_upper  <- NA_real_
}

writeLines(toJSON(out, auto_unbox = TRUE, na = "null", digits = 8), out_json)
