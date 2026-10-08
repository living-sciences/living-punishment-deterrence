#!/usr/bin/env Rscript
# Step 3: Table 3 - RD effect of exceeding the 0.08 DUI threshold on 4-yr recidivism.
suppressMessages({library(fixest); library(dplyr); library(jsonlite)})

df <- readRDS("outputs/rd_data.rds")
baseline <- fromJSON("outputs/baseline.json")$baseline_mean_recid

# Equation (1), local-linear RD, rectangular kernel = OLS on in-bandwidth sample.
# Controls: gender (male), race (white), age FE, year FE. County + prior-offense
# controls absent in this subset -> omitted (Appendix Table 1: results ~equivalent
# without controls).
fit_panel <- function(data, lo, hi) {
  d <- data %>% filter(bac >= lo, bac <= hi)
  m <- feols(recidivism ~ DUI + bac_c08 + DUI:bac_c08 + male + white +
               factor(aged) + factor(year),
             data = d, cluster = ~low_score)
  ct <- coeftable(m)["DUI", ]
  list(dui_coef = unname(ct["Estimate"]),
       se       = unname(ct["Std. Error"]),
       pval     = unname(ct["Pr(>|t|)"]),
       n        = nobs(m))
}

panelA <- fit_panel(df, 0.03, 0.13)    # bandwidth 0.05
panelB <- fit_panel(df, 0.055, 0.105)  # bandwidth 0.025

# Percent reduction = mean(Panel A, B DUI coef) / baseline (as a percent).
pct_reduction_all <- (mean(c(panelA$dui_coef, panelB$dui_coef)) / baseline) * 100

out <- list(
  panelA = panelA, panelB = panelB,
  baseline_mean_recid = baseline,
  pct_reduction_all = pct_reduction_all,
  note = paste("Cols (2) 'no prior tests' and (3) 'at least one prior test' of",
               "Table 3 CANNOT be reproduced: the Mixtape subset lacks the",
               "prior-test count variable. Only the 'all drivers' axis is run.",
               "County + prior controls also absent; omitted per Appendix Table 1.")
)
write_json(out, "outputs/table3.json", auto_unbox = TRUE, pretty = TRUE)
cat("Panel A: DUI =", panelA$dui_coef, "SE =", panelA$se, "N =", panelA$n, "\n")
cat("Panel B: DUI =", panelB$dui_coef, "SE =", panelB$se, "N =", panelB$n, "\n")
cat("pct_reduction_all:", pct_reduction_all, "\n")
