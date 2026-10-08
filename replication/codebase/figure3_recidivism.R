#!/usr/bin/env Rscript
# Step 9: Figure 3 - binned recidivism vs BAC with segmented RD fits, all offenders.
suppressMessages({library(dplyr); library(ggplot2)})

df <- readRDS("outputs/rd_data.rds")

win_lo <- 0.03; win_hi <- 0.20
d <- df %>% filter(bac >= win_lo, bac <= win_hi)

bw <- 0.002
d$bin <- floor(d$bac / bw) * bw + bw/2
binned <- d %>% group_by(bin) %>%
  summarise(recid = mean(recidivism), n = n(), .groups = "drop")

seg_breaks <- list(c(0.03, 0.08), c(0.08, 0.15), c(0.15, 0.20))
fits <- do.call(rbind, lapply(seg_breaks, function(b) {
  s <- d %>% filter(bac >= b[1], bac < b[2])
  m <- lm(recidivism ~ bac, data = s)
  grid <- data.frame(bac = seq(b[1], b[2], length.out = 50))
  grid$fit <- predict(m, grid); grid
}))

p <- ggplot() +
  geom_point(data = binned, aes(bin, recid), size = 1.1, colour = "grey35") +
  geom_line(data = fits, aes(bac, fit), colour = "black") +
  geom_vline(xintercept = c(0.08, 0.15), linetype = "dashed") +
  labs(x = "BAC", y = "Recidivism (4-year)",
       title = "Figure 3. Recidivism vs BAC, all offenders",
       subtitle = "Binned means (binwidth 0.002) with segmented local-linear RD fits") +
  theme_minimal(base_size = 12)

ggsave("outputs/figure3_recidivism.pdf", p, width = 8, height = 5.5)
ggsave("outputs/figure3_recidivism.png", p, width = 8, height = 5.5, dpi = 150)
cat("Figure 3 written (all offenders). First-time/repeat panels not reproducible (no prior var).\n")
