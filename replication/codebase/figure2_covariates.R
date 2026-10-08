#!/usr/bin/env Rscript
# Step 8: Figure 2 - binned means of predetermined characteristics vs BAC with
# segmented local-linear RD fits (below 0.08, [0.08,0.15), >=0.15).
suppressMessages({library(dplyr); library(ggplot2); library(tidyr)})

df <- readRDS("outputs/rd_data.rds")

covs <- c(male = "male", white = "white", aged = "aged", acc = "acc")
labels <- c(male = "Male", white = "White", aged = "Age", acc = "Accident")

win_lo <- 0.03; win_hi <- 0.20
d <- df %>% filter(bac >= win_lo, bac <= win_hi)

# Binned means at binwidth 0.002.
bw <- 0.002
d$bin <- floor(d$bac / bw) * bw + bw/2
binned <- d %>% group_by(bin) %>%
  summarise(across(all_of(unname(covs)), ~mean(.x)), .groups = "drop") %>%
  pivot_longer(-bin, names_to = "var", values_to = "mean")

# Segmented local-linear fits from eq (1) applied per covariate.
seg_breaks <- list(c(0.03, 0.08), c(0.08, 0.15), c(0.15, 0.20))
fit_segments <- function(yvar) {
  out <- lapply(seg_breaks, function(b) {
    s <- d %>% filter(bac >= b[1], bac < b[2])
    m <- lm(reformulate("bac", yvar), data = s)
    grid <- data.frame(bac = seq(b[1], b[2], length.out = 50))
    grid$fit <- predict(m, grid); grid$var <- yvar; grid
  })
  do.call(rbind, out)
}
fits <- do.call(rbind, lapply(unname(covs), fit_segments))

# Pretty facet labels
binned$var <- factor(binned$var, levels = unname(covs), labels = labels[names(covs)])
fits$var   <- factor(fits$var,   levels = unname(covs), labels = labels[names(covs)])

p <- ggplot() +
  geom_point(data = binned, aes(bin, mean), size = 0.8, colour = "grey40") +
  geom_line(data = fits, aes(bac, fit), colour = "black") +
  geom_vline(xintercept = c(0.08, 0.15), linetype = "dashed") +
  facet_wrap(~var, scales = "free_y") +
  labs(x = "BAC", y = "Mean of characteristic",
       title = "Figure 2. Predetermined characteristics vs BAC",
       subtitle = "Binned means (binwidth 0.002) with segmented local-linear RD fits") +
  theme_minimal(base_size = 11)

ggsave("outputs/figure2_covariates.pdf", p, width = 9, height = 6.5)
ggsave("outputs/figure2_covariates.png", p, width = 9, height = 6.5, dpi = 150)
cat("Figure 2 written (male, white, age, accident). Prior/PBT panels not reproducible (absent).\n")
