#!/usr/bin/env Rscript
# Panel B1 heaping + B2 gender balance (Florida).
.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))
suppressMessages({library(rddensity); library(rdrobust)})
RES <- "/workspace/eval/followup/002-methods-and-transport/results"
fl <- read.csv("/workspace/eval/followup/002-methods-and-transport/workspace/data/fl_analysis.csv")
wa <- readRDS("/workspace/eval/replication/codebase/outputs/rd_data.rds")

# ---- heaping: share at exact cutoff bin vs mean of 5 bins each side ----
share_at <- function(low_score, c0) {
  tab <- table(low_score); n <- length(low_score)
  cnt <- function(s){v<-tab[as.character(s)]; if(is.na(v)) 0 else as.numeric(v)}
  at <- cnt(c0)/n
  nb <- mean(sapply(c((c0-5):(c0-1),(c0+1):(c0+5)), cnt))/n
  c(share_at=at, mean_neighbor_share=nb, ratio=at/nb, count_at=cnt(c0))
}
hp <- rbind(
  data.frame(state="FL",threshold=0.08,t(share_at(fl$low_score,80))),
  data.frame(state="FL",threshold=0.15,t(share_at(fl$low_score,150))),
  data.frame(state="WA",threshold=0.08,t(share_at(wa$low_score,80))),
  data.frame(state="WA",threshold=0.15,t(share_at(wa$low_score,150))))
write.csv(hp, file.path(RES,"florida_heaping_shares.csv"), row.names=FALSE)
cat("=== heaping: cutoff-bin share vs neighbor mean ===\n"); print(hp)

# ---- last-digit distribution (0.001 units) + chi-square vs uniform ----
lastdigit_chisq <- function(ls) {
  d <- ls %% 10
  tabd <- table(factor(d, levels=0:9))
  ct <- chisq.test(as.numeric(tabd))
  list(counts=as.numeric(tabd), p=ct$p.value, stat=unname(ct$statistic))
}
ld_rows <- list()
for (nm in c("ls_s1","ls_s1")) {}  # placeholder
for (samp in c("ls_s1")) {}
ld <- list(
  FL_sample1 = lastdigit_chisq(fl$ls_s1),
  FL_sample2 = lastdigit_chisq(round(fl$sample2*1000)),
  WA_lowscore = lastdigit_chisq(wa$low_score))
ldf <- do.call(rbind, lapply(names(ld), function(k)
  data.frame(series=k, digit=0:9, count=ld[[k]]$counts,
             chisq=ld[[k]]$stat, p=ld[[k]]$p)))
write.csv(ldf, file.path(RES,"florida_lastdigit.csv"), row.names=FALSE)
cat("\n=== last-digit chi-square vs uniform ===\n")
for (k in names(ld)) cat(sprintf("  %-12s chisq=%.1f p=%.3g digits(share%%): %s\n", k, ld[[k]]$stat, ld[[k]]$p,
    paste(sprintf("%.1f", 100*ld[[k]]$counts/sum(ld[[k]]$counts)), collapse=" ")))

# per top-3 instrument pseudonyms (most tests), sample1 last digit
topi <- names(sort(table(fl$instrument_pseudonym), decreasing=TRUE))[1:3]
cat("\n=== last-digit chi-square for top-3 instruments (sample1) ===\n")
inst_rows <- list()
for (ins in topi) {
  sub <- fl$ls_s1[fl$instrument_pseudonym==as.integer(ins)]
  r <- lastdigit_chisq(sub)
  cat(sprintf("  instrument %s  n=%d  chisq=%.1f p=%.3g\n", ins, length(sub), r$stat, r$p))
  inst_rows[[length(inst_rows)+1]] <- data.frame(instrument=ins, n=length(sub), chisq=r$stat, p=r$p,
    t(setNames(r$counts, paste0("d",0:9))))
}
write.csv(do.call(rbind,inst_rows), file.path(RES,"florida_lastdigit_byinstrument.csv"), row.names=FALSE)

# ---- donut re-run: drop cutoff bin (and heaped round bins) and re-test density ----
donut_density <- function(x_units, c0, drop) {
  keep <- !(x_units %in% drop)
  r <- rddensity((x_units[keep])/1000, c=c0/1000, massPoints=TRUE)
  c(p_jk=r$test$p_jk, t_jk=r$test$t_jk)
}
dd <- rbind(
  data.frame(threshold=0.08, drop="cutoff bin (80)", t(donut_density(fl$low_score,80,c(80)))),
  data.frame(threshold=0.15, drop="cutoff bin (150)", t(donut_density(fl$low_score,150,c(150)))),
  data.frame(threshold=0.08, drop="round bins (80,90,100...)", t(donut_density(fl$low_score,80, seq(0,500,10)))),
  data.frame(threshold=0.15, drop="round bins", t(donut_density(fl$low_score,150, seq(0,500,10)))))
write.csv(dd, file.path(RES,"florida_density_donut.csv"), row.names=FALSE)
cat("\n=== donut density re-run (FL) ===\n"); print(dd)

# ---- B2 gender balance: A1 (rdrobust) outcome=male ----
balrow <- function(x, male, cc) {
  o <- rdrobust(male, x, c=cc, p=1, kernel="triangular", bwselect="mserd", vce="hc1", masspoints="adjust")
  data.frame(threshold=ifelse(cc<0.1,0.08,0.15), est=unname(o$coef[1]), se=unname(o$se[1]),
             ci_lo=unname(o$ci["Robust",1]), ci_hi=unname(o$ci["Robust",2]), p=unname(o$pv["Robust",1]), h=o$bws[1,1])
}
gb <- rbind(balrow(fl$run_min, fl$male, 0.08), balrow(fl$run_min, fl$male, 0.15))
write.csv(gb, file.path(RES,"florida_gender_balance.csv"), row.names=FALSE)
cat("\n=== B2 FL gender balance (outcome=male, A1 estimator) ===\n"); print(gb)
cat("\nPanel B heaping/balance complete.\n")
