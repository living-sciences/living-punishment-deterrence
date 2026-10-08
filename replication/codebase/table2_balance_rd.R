#!/usr/bin/env Rscript
# Step 5: Table 2 - covariate smoothness (balance) RD at both thresholds.
suppressMessages({library(fixest); library(dplyr); library(jsonlite)})

df <- readRDS("outputs/rd_data.rds")

# Balance regressions follow eq (1) with NO controls (paper Table 2: "Controls No"),
# since the predetermined characteristics are themselves the dependent variables.
# bandwidth 0.05, rectangular kernel, clustered at integer low_score (0.001 bin).
covs <- c(male = "male", white = "white", age = "aged", accident = "acc")

run_balance <- function(data, lo, hi, treat, center, thr_lo, thr_hi) {
  d <- data %>% filter(bac >= lo, bac <= hi)
  res <- list()
  for (nm in names(covs)) {
    y <- covs[[nm]]
    f <- as.formula(sprintf("%s ~ %s + %s + %s:%s", y, treat, center, treat, center))
    m <- feols(f, data = d, cluster = ~low_score)
    ct <- coeftable(m)[treat, ]
    mean_left <- data %>% filter(bac >= thr_lo, bac <= thr_hi) %>% pull(!!y) %>% mean()
    res[[nm]] <- list(coef = unname(ct["Estimate"]),
                      se   = unname(ct["Std. Error"]),
                      mean_at_threshold = mean_left)
  }
  res
}

# Panel A: DUI threshold 0.08, bw 0.05 -> [0.03,0.13]; mean just-left in [0.03,0.079].
panelA <- run_balance(df, 0.03, 0.13, "DUI", "bac_c08", 0.03, 0.079)
# Panel B: AGG threshold 0.15, bw 0.05 -> [0.10,0.20]; mean just-left in [0.10,0.149].
panelB <- run_balance(df, 0.10, 0.20, "AGG", "bac_c15", 0.10, 0.149)

out <- list(panelA = panelA, panelB = panelB,
            note = paste("Paper's 'Prior' (col 5) and 'PBT' (col 6) columns of Table 2",
                         "CANNOT be reproduced: those variables are absent from the",
                         "Mixtape subset. Only male/white/age/accident are tested.",
                         "No controls included (matches paper 'Controls No')."))
write_json(out, "outputs/table2.json", auto_unbox = TRUE, pretty = TRUE)

cat("Panel A (DUI 0.08):\n")
for (nm in names(panelA)) cat(sprintf("  %-9s coef=%+.5f se=%.5f mean=%.4f\n",
    nm, panelA[[nm]]$coef, panelA[[nm]]$se, panelA[[nm]]$mean_at_threshold))
cat("Panel B (AGG 0.15):\n")
for (nm in names(panelB)) cat(sprintf("  %-9s coef=%+.5f se=%.5f mean=%.4f\n",
    nm, panelB[[nm]]$coef, panelB[[nm]]$se, panelB[[nm]]$mean_at_threshold))
