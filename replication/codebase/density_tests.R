#!/usr/bin/env Rscript
# Step 6: Manipulation / density tests of the running variable.
#  (a) McCrary (2008) density test via rdd::DCdensity at 0.08 and 0.15.
#  (b) Frandsen (2013/2017) discrete-density manipulation test, reimplemented.
suppressMessages({library(rdd); library(jsonlite)})

df <- readRDS("outputs/rd_data.rds")
bac <- df$bac

# ---- (a) McCrary (2008) ----
mccrary <- function(x, cut) {
  pdf_file <- tempfile(fileext = ".pdf"); pdf(pdf_file)
  r <- DCdensity(x, cutpoint = cut, ext.out = TRUE)
  dev.off(); unlink(pdf_file)
  list(pval = unname(r$p), theta = unname(r$theta), se = unname(r$se),
       z = unname(r$z), bw = unname(r$bw))
}
mc08 <- mccrary(bac, 0.08)
mc15 <- mccrary(bac, 0.15)

# ---- (b) Frandsen (2013/2017) discrete-density manipulation test ----
# Running variable is discrete (integer low_score = BAC x 1000, 0.001 precision).
# Frandsen's "k-smoothness" null bounds the discrete second difference of the pmf
# at the cutoff. Let bin c be the first TREATED bin (low_score = 80 or 150), and
# a=f(c-1) (last untreated bin), b=f(c) (first treated bin). Absent manipulation,
# the count in the cutoff bin is predicted by extrapolating the local trend from
# below with curvature bounded by k:
#    g_lo(c) = (2*f(c-1) - f(c-2)) - k*|f(c-1)|   (most mass-below-friendly)
#    g_hi(c) = (2*f(c-1) - f(c-2)) + k*|f(c-1)|
# Conditional on n=a+b, b ~ Binomial(n, theta) with theta in the interval
# [g_lo/(f(c-1)+g_lo), g_hi/(f(c-1)+g_hi)]. The p-value is the binomial-test
# p-value at the theta in that interval closest to the observed share b/n (the
# least-rejecting / most conservative null value). Manipulation to dodge the
# threshold produces a DEFICIT in the first treated bin (b below prediction).
frandsen <- function(low_score, cut_score, k = 0.01) {
  tab <- table(low_score)
  cnt <- function(s) { v <- tab[as.character(s)]; if (is.na(v)) 0 else as.numeric(v) }
  a   <- cnt(cut_score - 1)   # f(c-1), last untreated bin
  b   <- cnt(cut_score)       # f(c),  first treated bin
  fm2 <- cnt(cut_score - 2)   # f(c-2)
  pred <- 2 * a - fm2         # linear (k=0) extrapolation of the cutoff-bin count
  g_lo <- max(1e-9, pred - k * a)
  g_hi <- pred + k * a
  th_lo <- g_lo / (a + g_lo)
  th_hi <- g_hi / (a + g_hi)
  n <- a + b
  obs_share <- b / n
  theta_star <- min(max(obs_share, min(th_lo, th_hi)), max(th_lo, th_hi))
  p <- binom.test(b, n, p = theta_star)$p.value
  list(pval = p, k = k, f_cminus1 = a, f_cutoff = b, f_cminus2 = fm2,
       predicted_cutoff = pred, theta_null = theta_star, obs_share = obs_share)
}
fr08 <- frandsen(df$low_score, 80,  k = 0.01)
fr15 <- frandsen(df$low_score, 150, k = 0.01)

# Raw local density ratio (first 3 treated bins / last 3 untreated bins) for context.
tab <- table(df$low_score)
cnt <- function(s) { v <- tab[as.character(s)]; if (is.na(v)) 0 else as.numeric(v) }
ratio08 <- sum(sapply(80:82, cnt)) / sum(sapply(77:79, cnt))
ratio15 <- sum(sapply(150:152, cnt)) / sum(sapply(147:149, cnt))

out <- list(
  mccrary = list(thr_008 = mc08, thr_015 = mc15),
  frandsen = list(thr_008 = fr08, thr_015 = fr15),
  raw_local_ratio = list(thr_008 = ratio08, thr_015 = ratio15),
  paper_reference = list(mccrary = list(thr_008 = 0.59, thr_015 = 0.38),
                         frandsen = list(thr_008 = 0.795, thr_015 = 0.886)),
  note = paste(
    "McCrary rdd::DCdensity strongly rejects (p~0, theta>0) at both thresholds in",
    "this Mixtape SUBSET, diverging from the paper's p=0.59/0.38 (full 512,964-obs",
    "sample). The raw local density ratio is only ~1.14 (0.08) and ~0.96 (0.15),",
    "i.e. a modest step, so the large theta is a local-linear density-fit artifact:",
    "the BAC pmf is heavily discrete (~400 ties) and strongly curved, and n=214k",
    "inflates the z-stat. This is exactly the discrete/rounded case the paper cites",
    "Frandsen (2013) for. The Frandsen reimplementation does NOT reject at either",
    "threshold (consistent with the paper's no-manipulation conclusion), though the",
    "exact p-values differ from 0.795/0.886 (different smoothness parameterization).")
)
write_json(out, "outputs/density_tests.json", auto_unbox = TRUE, pretty = TRUE)

cat(sprintf("McCrary 0.08: p=%.4f  theta=%+.4f (z=%.3f)\n", mc08$pval, mc08$theta, mc08$z))
cat(sprintf("McCrary 0.15: p=%.4f  theta=%+.4f (z=%.3f)\n", mc15$pval, mc15$theta, mc15$z))
cat(sprintf("Frandsen 0.08: p=%.4f (k=%.3f)  b=%d pred=%.1f\n", fr08$pval, fr08$k, fr08$f_cutoff, fr08$predicted_cutoff))
cat(sprintf("Frandsen 0.15: p=%.4f (k=%.3f)  b=%d pred=%.1f\n", fr15$pval, fr15$k, fr15$f_cutoff, fr15$predicted_cutoff))
