#!/usr/bin/env Rscript
# Step 7: Figure 1 - histogram of BAC over 1999-2007, binwidth 0.001.
suppressMessages({library(ggplot2)})

df <- readRDS("outputs/rd_data.rds")

p <- ggplot(df, aes(x = bac)) +
  geom_histogram(binwidth = 0.001, boundary = 0, fill = "grey35", colour = NA) +
  geom_vline(xintercept = c(0.08, 0.15), linetype = "solid", colour = "black") +
  coord_cartesian(xlim = c(0, 0.4)) +
  labs(x = "BAC", y = "Frequency",
       title = "Figure 1. BAC Distribution (1999-2007)",
       subtitle = "Bin width 0.001; vertical lines at 0.08 and 0.15") +
  theme_minimal(base_size = 12)

ggsave("outputs/figure1_bac_histogram.pdf", p, width = 8, height = 5)
ggsave("outputs/figure1_bac_histogram.png", p, width = 8, height = 5, dpi = 150)
cat("Figure 1 written. n =", nrow(df), "\n")
