# Full GAMLSS (BCCG / LMS) national reference: fit on the complete healthy subset,
# score the full analytic sample, and export z-scores, LLN, centile grid and the
# L/M/S table. BCCGo models median (mu=M, log link), coefficient of variation
# (sigma=S) and skewness (nu=L) as penalized-spline functions of age; log-height
# enters mu multiplicatively for volumes.
userlib <- path.expand("~/R/win-library"); .libPaths(c(userlib, .libPaths()))
suppressMessages({library(gamlss); library(gamlss.dist)})

here <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value=TRUE)))
if (length(here)==0 || here=="") here <- "."
outdir <- file.path(here, "..", "outputs")
H <- read.csv(file.path(outdir, "healthy_subset.csv")); H$lnht <- log(H$height)
A <- read.csv(file.path(outdir, "analytic_full.csv")); A$lnht <- log(A$height)
refht <- c(M=median(H$height[H$sex=="M"]), F=median(H$height[H$sex=="F"]))

params <- c("fvc","fev1","fev1fvc")
scored <- A
centile <- list(); lms <- list()
for (p in params) {
  for (s in c("M","F")) {
    tr <- subset(H, sex==s); tr$y <- tr[[p]]
    form <- if (p=="fev1fvc") y ~ pb(age) else y ~ pb(age) + lnht
    m <- gamlss(form, sigma.fo=~pb(age), nu.fo=~pb(age), family=BCCGo,
                data=tr, control=gamlss.control(trace=FALSE))
    idx <- which(A$sex==s)
    nd <- A[idx, c("age","lnht")]
    pr <- predictAll(m, newdata=nd, data=tr, type="response")
    y <- A[[p]][idx]
    scored[idx, paste0(p,"_M")]   <- round(pr$mu, 4)
    scored[idx, paste0(p,"_z")]   <- round(qNO(pBCCGo(y, mu=pr$mu, sigma=pr$sigma, nu=pr$nu)), 4)
    scored[idx, paste0(p,"_lln")] <- round(qBCCGo(0.05, mu=pr$mu, sigma=pr$sigma, nu=pr$nu), 4)
    # centile grid + LMS table at reference height, ages 45..90
    ages <- 45:90
    gd <- data.frame(age=ages, lnht=log(refht[[s]]))
    gp <- predictAll(m, newdata=gd, data=tr, type="response")
    if (p!="fev1fvc") {
      centile[[paste(p,s)]] <- data.frame(param=p, sex=s, refht=round(refht[[s]],1),
        age=ages, median=round(gp$mu,3),
        lln=round(qBCCGo(0.05, mu=gp$mu, sigma=gp$sigma, nu=gp$nu),3))
    }
    bht <- if (p=="fev1fvc") NA else round(as.numeric(coef(m,"mu")["lnht"]),4)
    lms[[paste(p,s)]] <- data.frame(param=p, sex=s, refht=round(refht[[s]],1), lnht_coef=bht,
      age=ages, L=round(gp$nu,4), M=round(gp$mu,4), S=round(gp$sigma,4))
    cat(sprintf("fitted %s %s (GAIC %.1f)\n", p, s, GAIC(m)))
  }
}
write.csv(scored, file.path(outdir, "scored_gamlss.csv"), row.names=FALSE)
write.csv(do.call(rbind, centile), file.path(here,"gamlss_centile_grid.csv"), row.names=FALSE)
write.csv(do.call(rbind, lms), file.path(here,"gamlss_LMS_table.csv"), row.names=FALSE)
cat("DONE: scored analytic, centile grid, LMS table written.\n")
