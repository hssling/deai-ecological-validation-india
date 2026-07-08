# GAMLSS (BCCG / LMS) reference-equation refinement for LASI national spirometry.
# BCCG models median (mu=M), coefficient of variation (sigma=S) and skewness
# (nu=L) as penalized-spline functions of age, with log-height as a linear term
# for volumes. Validated on a held-out 20% sample: z should be ~N(0,1).
userlib <- path.expand("~/R/win-library"); .libPaths(c(userlib, .libPaths()))
suppressMessages({library(gamlss); library(gamlss.dist)})

here <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value=TRUE)))
if (length(here)==0 || here=="") here <- "."
csv <- file.path(here, "..", "outputs", "healthy_subset.csv")
d <- read.csv(csv)
d$lnht <- log(d$height)

fit_one <- function(param, sexcode) {
  tr <- subset(d, sex==sexcode & split=="train")
  te <- subset(d, sex==sexcode & split=="test")
  tr$y <- tr[[param]]; te$y <- te[[param]]
  # volumes: log-height covariate in mu; ratio: age only
  if (param=="fev1fvc") {
    form_mu <- y ~ pb(age)
  } else {
    form_mu <- y ~ pb(age) + lnht
  }
  m <- gamlss(form_mu, sigma.fo=~pb(age), nu.fo=~pb(age),
              family=BCCGo, data=tr, control=gamlss.control(trace=FALSE))
  # z-scores on held-out test set
  pr <- predictAll(m, newdata=te[, c("age","lnht")], data=tr, type="response")
  z <- qNO(pBCCGo(te$y, mu=pr$mu, sigma=pr$sigma, nu=pr$nu))
  z <- z[is.finite(z)]
  data.frame(param=param, sex=sexcode, n_test=length(z),
             mean_z=round(mean(z),3), sd_z=round(sd(z),3),
             GAIC=round(GAIC(m),1))
}

res <- do.call(rbind, list(
  fit_one("fvc","M"), fit_one("fvc","F"),
  fit_one("fev1","M"), fit_one("fev1","F"),
  fit_one("fev1fvc","M"), fit_one("fev1fvc","F")
))
cat("\n===== GAMLSS BCCG (LMS) held-out validation =====\n")
print(res, row.names=FALSE)
write.csv(res, file.path(here, "gamlss_validation.csv"), row.names=FALSE)
cat("\nOK: gamlss fit + holdout z computed.\n")
