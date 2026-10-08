#!/usr/bin/env Rscript
# Panel A: Washington 1999-2007 methods re-analysis (Hansen 2015 follow-up 001).
# Branch N (do-files NOT obtained): 0.15 reported under BOTH codings, co-equal.
.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))
suppressMessages({library(rdrobust); library(RDHonest); library(fixest); library(dplyr); library(jsonlite)})
set.seed(1)

RES <- "/workspace/eval/followup/002-methods-and-transport/results"
dir.create(RES, showWarnings = FALSE, recursive = TRUE)
df <- readRDS("/workspace/eval/replication/codebase/outputs/rd_data.rds")

# Bin means confirmed in gate 2 (used by 002 later; recorded here).
mean79  <- mean(df$recidivism[df$low_score == 79])
mean149 <- mean(df$recidivism[df$low_score == 149])

# Covariate matrix for rdrobust covariate-adjusted spec: male, white, age, year dummies.
ydum <- model.matrix(~ factor(year), df)[, -1, drop = FALSE]
COVS <- cbind(male = df$male, white = df$white, age = df$aged, ydum)

# ---- helpers ------------------------------------------------------------
# cutoff c for rdrobust: statutory uses c0; strict (treated if L>=c0+1) uses c0+0.0005
masspt_counts <- function(bac, cc, hl, hr) {
  left  <- length(unique(bac[bac >= cc - hl & bac < cc]))
  right <- length(unique(bac[bac >= cc & bac <= cc + hr]))
  c(left = left, right = right)
}

run_rdrobust <- function(cc, bwsel = "mserd", covs = NULL) {
  o <- rdrobust(df$recidivism, df$bac, c = cc, p = 1, kernel = "triangular",
                bwselect = bwsel, vce = "hc1", masspoints = "adjust", covs = covs)
  hl <- o$bws[1, 1]; hr <- o$bws[1, 2]
  mp <- masspt_counts(df$bac, cc, hl, hr)
  list(coef = unname(o$coef[1]), se = unname(o$se[1]),
       ci_rbc_lo = unname(o$ci["Robust", 1]), ci_rbc_hi = unname(o$ci["Robust", 2]),
       h = hl, b = o$bws[2, 1], N_l = unname(o$N_h[1]), N_r = unname(o$N_h[2]),
       mp_l = unname(mp["left"]), mp_r = unname(mp["right"]),
       pv_rbc = unname(o$pv["Robust", 1]))
}

run_rdhonest <- function(cc, Mmult = 1, Mfix = NULL) {
  if (is.null(Mfix)) {
    h <- RDHonest(recidivism ~ bac, data = df, cutoff = cc, kern = "triangular", opt.criterion = "MSE")
    Mrot <- h$coefficients$M
    if (Mmult != 1) h <- RDHonest(recidivism ~ bac, data = df, cutoff = cc, kern = "triangular",
                                  opt.criterion = "MSE", M = Mmult * Mrot)
  } else {
    h <- RDHonest(recidivism ~ bac, data = df, cutoff = cc, kern = "triangular",
                  opt.criterion = "MSE", M = Mfix)
  }
  cf <- h$coefficients
  list(est = cf$estimate, se = cf$std.error, bias = cf$maximum.bias,
       ci_lo = cf$conf.low, ci_hi = cf$conf.high, h = cf$bandwidth,
       M = cf$M, pv = cf$p.value)
}

# A0: paper-method OLS (rectangular kernel = OLS in window), cluster on low_score.
run_A0 <- function(treatvar, centervar, lo, hi, controls = TRUE) {
  d <- df %>% filter(bac >= lo, bac <= hi)
  rhs <- sprintf("%s + %s + %s:%s", treatvar, centervar, treatvar, centervar)
  if (controls) rhs <- paste(rhs, "+ male + white + factor(aged) + factor(year)")
  m <- feols(as.formula(paste("recidivism ~", rhs)), data = d, cluster = ~low_score)
  ct <- coeftable(m)[treatvar, ]
  list(coef = unname(ct[1]), se = unname(ct[2]), pval = unname(ct[4]), n = nobs(m))
}

# treatment indicators for A0 under each coding
df$DUIs  <- as.integer(df$bac >= 0.08)   # statutory 0.08
df$DUIx  <- as.integer(df$bac >= 0.081)  # strict 0.08
df$AGGs  <- as.integer(df$bac >= 0.15)   # statutory 0.15
df$AGGx  <- as.integer(df$bac >= 0.151)  # strict 0.15

# specs: label, threshold, coding, c0, rd cutoff, A0 treatvar, A0 window(bw0.05 & 0.025)
specs <- list(
  list(lab = "0.08_statutory", thr = 0.08, coding = "statutory", cc = 0.08,   tv = "DUIs", cv = "bac_c08", w05 = c(0.03,0.13),  w025 = c(0.055,0.105)),
  list(lab = "0.15_statutory", thr = 0.15, coding = "statutory", cc = 0.15,   tv = "AGGs", cv = "bac_c15", w05 = c(0.10,0.20),  w025 = c(0.125,0.175)),
  list(lab = "0.15_strict",    thr = 0.15, coding = "strict",    cc = 0.1505, tv = "AGGx", cv = "bac_c15", w05 = c(0.10,0.20),  w025 = c(0.125,0.175))
)

headline <- list()
scalars <- list(mean_at_079 = mean79, mean_at_149 = mean149,
                packages = list(rdrobust = as.character(packageVersion("rdrobust")),
                                rddensity = as.character(packageVersion("rddensity")),
                                RDHonest = as.character(packageVersion("RDHonest")),
                                masspoints = "adjust"))

for (s in specs) {
  cat("=== spec", s$lab, "===\n")
  # A0 both windows, with and without controls
  a0_05  <- run_A0(s$tv, s$cv, s$w05[1],  s$w05[2],  TRUE)
  a0_05n <- run_A0(s$tv, s$cv, s$w05[1],  s$w05[2],  FALSE)
  a0_025 <- run_A0(s$tv, s$cv, s$w025[1], s$w025[2], TRUE)
  a0_025n<- run_A0(s$tv, s$cv, s$w025[1], s$w025[2], FALSE)
  # A1 RBC mserd (no covs) + covariate-adjusted + cerrd
  a1    <- run_rdrobust(s$cc, "mserd", NULL)
  a1cov <- run_rdrobust(s$cc, "mserd", COVS)
  a1cer <- run_rdrobust(s$cc, "cerrd", NULL)
  # A2 honest
  a2   <- run_rdhonest(s$cc, 1)
  a2_2 <- run_rdhonest(s$cc, 2)

  headline[[s$lab]] <- list(threshold = s$thr, coding = s$coding,
    A0_bw05 = a0_05, A0_bw05_nocov = a0_05n, A0_bw025 = a0_025, A0_bw025_nocov = a0_025n,
    A1 = a1, A1_cov = a1cov, A1_cerrd = a1cer, A2 = a2, A2_2M = a2_2)

  cat(sprintf("  A0bw05 %.4f(%.4f) N=%d | A1 %.4f(%.4f) RBC[%.4f,%.4f] h=%.4f mp %d/%d | A2 %.4f honest[%.4f,%.4f] M=%.1f h=%.4f\n",
    a0_05$coef, a0_05$se, a0_05$n, a1$coef, a1$se, a1$ci_rbc_lo, a1$ci_rbc_hi, a1$h, a1$mp_l, a1$mp_r,
    a2$est, a2$ci_lo, a2$ci_hi, a2$M, a2$h))
}

saveRDS(headline, file.path(RES, "_headline_raw.rds"))
write_json(c(list(headline = headline), scalars), file.path(RES, "headline_scalars.json"),
           auto_unbox = TRUE, pretty = TRUE, digits = 8)

# ---- build estimates_headline.csv --------------------------------------
rows <- list()
addrow <- function(thr, coding, est, h, M, estimate, se, lo, hi, mpl, mpr, nl, nr, vr) {
  rows[[length(rows)+1]] <<- data.frame(threshold=thr, coding=coding, estimator=est,
    h=h, M=M, estimate=estimate, se=se, ci_low=lo, ci_high=hi,
    ci_width=hi-lo, mass_points_left=mpl, mass_points_right=mpr,
    N_left=nl, N_right=nr, verdict_row=vr, stringsAsFactors=FALSE)
}
for (s in specs) {
  H <- headline[[s$lab]]
  a0 <- H$A0_bw05; a1 <- H$A1; a2 <- H$A2
  # verdict row logic: A1 RBC CI and A2 honest CI
  a1_excl <- (a1$ci_rbc_lo > 0) | (a1$ci_rbc_hi < 0)
  a2_excl <- (a2$ci_lo > 0) | (a2$ci_hi < 0)
  vr <- if (a1_excl & a2_excl) "both_exclude" else if (!a1_excl & !a2_excl) "both_include" else "mixed"
  addrow(s$thr, s$coding, "A0_paper_bw05", 0.05, NA, a0$coef, a0$se, a0$coef-1.96*a0$se, a0$coef+1.96*a0$se, NA, NA, NA, NA, vr)
  addrow(s$thr, s$coding, "A1_RBC", a1$h, NA, a1$coef, a1$se, a1$ci_rbc_lo, a1$ci_rbc_hi, a1$mp_l, a1$mp_r, a1$N_l, a1$N_r, vr)
  addrow(s$thr, s$coding, "A2_honest", a2$h, a2$M, a2$est, a2$se, a2$ci_lo, a2$ci_hi, NA, NA, NA, NA, vr)
}
hd <- do.call(rbind, rows)
write.csv(hd, file.path(RES, "estimates_headline.csv"), row.names = FALSE)
cat("\nwrote estimates_headline.csv\n"); print(hd[,c("threshold","coding","estimator","estimate","ci_low","ci_high","verdict_row")])
cat("\nPanel A core done.\n")
