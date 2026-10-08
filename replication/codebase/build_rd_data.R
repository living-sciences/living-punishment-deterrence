#!/usr/bin/env Rscript
# Step 2: Build the RD analysis dataset and baseline recidivism rate.
suppressMessages({library(haven); library(dplyr); library(jsonlite)})

dir.create("outputs", showWarnings = FALSE)

df <- read_dta("data/hansen_dwi.dta")

# Running variable in BAC units from the paper's min-of-two-readings score.
# Per DATA_README, low_score = min(Alcohol1, Alcohol2) (BAC x 1000).
stopifnot(all(df$low_score == pmin(df$Alcohol1, df$Alcohol2)))
df$bac <- df$low_score / 1000

# Treatments at the two legal thresholds.
df$DUI <- as.integer(df$bac >= 0.08)
df$AGG <- as.integer(df$bac >= 0.15)

# Centered running variables.
df$bac_c08 <- df$bac - 0.08
df$bac_c15 <- df$bac - 0.15

# Paper's 1999-2007 estimation window.
df <- df %>% filter(year >= 1999, year <= 2007)

n_total <- nrow(df)

# Baseline left-of-0.08 recidivism for all tested drivers in the Panel A
# below-threshold window [0.03, 0.079].
below <- df %>% filter(bac >= 0.03, bac <= 0.079)
baseline_mean_recid <- mean(below$recidivism)

saveRDS(df, "outputs/rd_data.rds")
write_json(list(n_total = n_total,
                baseline_mean_recid = baseline_mean_recid,
                n_below_window = nrow(below)),
           "outputs/baseline.json", auto_unbox = TRUE, pretty = TRUE)

cat("n_total:", n_total, "\n")
cat("baseline_mean_recid [0.03,0.079]:", baseline_mean_recid, "\n")
cat("cols:", paste(c("bac","DUI","AGG","bac_c08","bac_c15") %in% names(df), collapse=" "), "\n")
