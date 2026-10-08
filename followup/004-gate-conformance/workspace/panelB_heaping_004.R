#!/usr/bin/env Rscript
# 004 corrective: Panel B1 heaping (CORRECTED: exclude 0.000 readings) + B2 gender balance,
# on DEDUPLICATED Florida data. The 002 "~21% last digit 0" was a 0.000-reading artifact.
.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))
suppressMessages({library(rddensity); library(rdrobust)})
RES <- "/workspace/eval/followup/004-gate-conformance/results"
fl <- read.csv("/workspace/eval/followup/004-gate-conformance/workspace/data/fl_analysis.csv")
wa <- readRDS("/workspace/eval/replication/codebase/outputs/rd_data.rds")
cat(sprintf("FL two-sample DUI rows (dedup): %d\n", nrow(fl)))

# ---- 0.000-reading artifact: share of tests with a zero sample reading ----
z1 <- mean(fl$sample1 == 0.000); z2 <- mean(fl$sample2 == 0.000)
zrun <- mean(fl$run_min == 0.000)
cat(sprintf("share sample1==0.000: %.4f | sample2==0.000: %.4f | run_min==0.000: %.4f\n", z1, z2, zrun))

# ---- last-digit distribution, INCLUDING vs EXCLUDING 0.000 readings ----
lastdigit <- function(ls) {
  d <- ls %% 10
  tabd <- table(factor(d, levels=0:9))
  ct <- chisq.test(as.numeric(tabd))
  list(counts=as.numeric(tabd), p=ct$p.value, stat=unname(ct$statistic), n=length(ls))
}
mk <- function(series, r) data.frame(series=series, digit=0:9, count=r$counts,
    share_pct=round(100*r$counts/sum(r$counts),3), n=r$n, chisq=round(r$stat,2), p=signif(r$p,4))
# sample1 (ls_s1), sample2, run_min, each incl/excl zeros
rows <- list()
add <- function(series, vec_units){ r<-lastdigit(vec_units); rows[[length(rows)+1]]<<-mk(series,r); r }
r_s1_in  <- add("FL_sample1_inclzero", fl$ls_s1)
r_s1_ex  <- add("FL_sample1_exclzero", fl$ls_s1[fl$sample1!=0])
r_s2_in  <- add("FL_sample2_inclzero", round(fl$sample2*1000))
r_s2_ex  <- add("FL_sample2_exclzero", round(fl$sample2[fl$sample2!=0]*1000))
r_wa     <- add("WA_lowscore", wa$low_score)
ldf <- do.call(rbind, rows)
write.csv(ldf, file.path(RES,"florida_lastdigit.csv"), row.names=FALSE)
cat("\n=== last-digit digit-0 share (%) ===\n")
for (nm in c("FL_sample1_inclzero","FL_sample1_exclzero","FL_sample2_inclzero","FL_sample2_exclzero","WA_lowscore")) {
  s <- ldf[ldf$series==nm & ldf$digit==0,]
  cat(sprintf("  %-22s digit0=%.2f%%  chisq=%.1f p=%.3g  n=%d\n", nm, s$share_pct, s$chisq, s$p, s$n))
}

# per top-3 instruments, sample1 last digit EXCLUDING zeros
topi <- names(sort(table(fl$instrument_pseudonym), decreasing=TRUE))[1:3]
cat("\n=== last-digit (excl zeros) top-3 instruments (sample1) ===\n")
inst_rows <- list()
for (ins in topi) {
  sub <- fl$ls_s1[fl$instrument_pseudonym==as.integer(ins) & fl$sample1!=0]
  r <- lastdigit(sub)
  d0 <- 100*r$counts[1]/sum(r$counts)
  cat(sprintf("  instrument %s n=%d digit0=%.2f%% chisq=%.1f p=%.3g\n", ins, length(sub), d0, r$stat, r$p))
  inst_rows[[length(inst_rows)+1]] <- data.frame(instrument=ins, n=length(sub), digit0_pct=round(d0,3),
    chisq=round(r$stat,2), p=signif(r$p,4), t(setNames(r$counts, paste0("d",0:9))))
}
write.csv(do.call(rbind,inst_rows), file.path(RES,"florida_lastdigit_byinstrument.csv"), row.names=FALSE)

# ---- round-value excess near thresholds: count at cutoff bins & neighbours (run_min, excl zeros) ----
# audit check: no round-value excess at thresholds. Report cutoff-bin ratio and the 0.070/0.090/0.100 bins.
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
cat("\n=== cutoff-bin share vs neighbor mean (run_min) ===\n"); print(hp)

# round-value check at 0.070/0.080/0.090/0.100/0.150 vs neighbour mean (count-based, run_min)
tab <- table(fl$low_score); cnt <- function(s){v<-tab[as.character(s)]; if(is.na(v)) 0 else as.numeric(v)}
roundchk <- do.call(rbind, lapply(c(70,80,90,100,150), function(c0){
  nb <- mean(sapply(c((c0-5):(c0-1),(c0+1):(c0+5)), cnt))
  data.frame(bin=c0/1000, count_at=cnt(c0), neighbor_mean=round(nb,1), ratio=round(cnt(c0)/nb,3))
}))
write.csv(roundchk, file.path(RES,"florida_roundvalue_check.csv"), row.names=FALSE)
cat("\n=== round-value excess check (run_min counts) ===\n"); print(roundchk)

# ---- donut density re-run (drop cutoff bin only; the all-round-bins donut is NOT motivated, dropped) ----
donut_density <- function(x_units, c0, drop) {
  keep <- !(x_units %in% drop)
  r <- rddensity((x_units[keep])/1000, c=c0/1000, massPoints=TRUE)
  c(p_jk=r$test$p_jk, t_jk=r$test$t_jk)
}
dd <- rbind(
  data.frame(threshold=0.08, drop="cutoff bin (80)", t(donut_density(fl$low_score,80,c(80)))),
  data.frame(threshold=0.15, drop="cutoff bin (150)", t(donut_density(fl$low_score,150,c(150)))))
write.csv(dd, file.path(RES,"florida_density_donut.csv"), row.names=FALSE)
cat("\n=== donut density re-run (drop cutoff bin only) ===\n"); print(dd)

# ---- B2 gender balance: A1 (rdrobust) outcome=male, DEDUP data ----
balrow <- function(x, male, cc) {
  o <- rdrobust(male, x, c=cc, p=1, kernel="triangular", bwselect="mserd", vce="hc1", masspoints="adjust")
  data.frame(threshold=ifelse(cc<0.1,0.08,0.15), est=unname(o$coef[1]), se=unname(o$se[1]),
             ci_lo=unname(o$ci["Robust",1]), ci_hi=unname(o$ci["Robust",2]), p=unname(o$pv["Robust",1]), h=o$bws[1,1])
}
gb <- rbind(balrow(fl$run_min, fl$male, 0.08), balrow(fl$run_min, fl$male, 0.15))
write.csv(gb, file.path(RES,"florida_gender_balance.csv"), row.names=FALSE)
cat("\n=== B2 FL gender balance (outcome=male, A1) DEDUP ===\n"); print(gb)
cat("\nPanel B heaping/balance (corrected) complete.\n")
