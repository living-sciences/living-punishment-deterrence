#!/usr/bin/env Rscript
# Step 4: Table 4 - RD effect of exceeding the 0.15 aggravated-DUI threshold.
suppressMessages({library(fixest); library(dplyr); library(jsonlite)})

df <- readRDS("outputs/rd_data.rds")

fit_panel <- function(data, lo, hi) {
  d <- data %>% filter(bac >= lo, bac <= hi)
  m <- feols(recidivism ~ AGG + bac_c15 + AGG:bac_c15 + male + white +
               factor(aged) + factor(year),
             data = d, cluster = ~low_score)
  ct <- coeftable(m)["AGG", ]
  list(agg_coef = unname(ct["Estimate"]),
       se       = unname(ct["Std. Error"]),
       pval     = unname(ct["Pr(>|t|)"]),
       n        = nobs(m))
}

panelA <- fit_panel(df, 0.10, 0.20)     # bandwidth 0.05
panelB <- fit_panel(df, 0.125, 0.175)   # bandwidth 0.025

# Baseline recidivism just left of 0.15 within the Panel A window.
baseline_left_015 <- df %>%
  filter(bac >= 0.10, bac <= 0.149) %>% pull(recidivism) %>% mean()

pct_reduction_all <- (mean(c(panelA$agg_coef, panelB$agg_coef)) / baseline_left_015) * 100

out <- list(
  panelA = panelA, panelB = panelB,
  baseline_left_015 = baseline_left_015,
  pct_reduction_all = pct_reduction_all,
  note = paste("Cols (2) 'no prior tests' and (3) 'at least one prior test' of",
               "Table 4 CANNOT be reproduced: subset lacks the prior-test variable.",
               "Only 'all drivers' is run. County/prior controls absent; omitted.")
)
write_json(out, "outputs/table4.json", auto_unbox = TRUE, pretty = TRUE)
cat("Panel A: AGG =", panelA$agg_coef, "SE =", panelA$se, "N =", panelA$n, "\n")
cat("Panel B: AGG =", panelB$agg_coef, "SE =", panelB$se, "N =", panelB$n, "\n")
cat("baseline_left_015:", baseline_left_015, " pct_reduction_all:", pct_reduction_all, "\n")
