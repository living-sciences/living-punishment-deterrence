#!/usr/bin/env Rscript
# Panel B1 + WA density comparison: rddensity, log-density jump, MDD, discrete test.
.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))
suppressMessages({library(rddensity); library(jsonlite)})
RES <- "/workspace/eval/followup/002-methods-and-transport/results"
wa <- readRDS("/workspace/eval/replication/codebase/outputs/rd_data.rds")
fl <- read.csv("/workspace/eval/followup/002-methods-and-transport/workspace/data/fl_analysis.csv")

# log-density jump + MDD from an rddensity fit
dens <- function(x, cc) {
  r <- rddensity(x, c=cc, massPoints=TRUE)
  fl_ <- r$hat$left; fr_ <- r$hat$right; diff <- r$hat$diff
  tjk <- r$test$t_jk; pjk <- r$test$p_jk
  se_diff <- abs(diff)/abs(tjk)
  favg <- (fl_+fr_)/2
  logjump <- log(fr_) - log(fl_)
  se_log <- se_diff/favg
  mdd <- (1.96+0.84)*se_log
  list(f_l=fl_, f_r=fr_, t_jk=tjk, p_jk=pjk,
       logjump=logjump, lo=logjump-1.96*se_log, hi=logjump+1.96*se_log,
       se_log=se_log, mdd=mdd, Nl=r$N$eff_left, Nr=r$N$eff_right)
}
# discrete binomial test (spirit of Frandsen): cutoff-bin count vs local-linear prediction
disc_test <- function(low_score, c0, k) {
  tab <- table(low_score); cnt <- function(s){ v<-tab[as.character(s)]; if(is.na(v)) 0 else as.numeric(v)}
  pos <- c((c0-k):(c0-1),(c0+1):(c0+k)); y <- sapply(pos,cnt); rel <- pos-c0
  fit <- lm(y~rel); pred <- max(as.numeric(predict(fit,newdata=data.frame(rel=0))),1)
  obs <- cnt(c0); n <- round(obs+pred)
  list(k=k, obs=obs, pred=pred, p=binom.test(obs,n,0.5)$p.value)
}

rows <- list()
adddens <- function(state, scope, thr, d) {
  rows[[length(rows)+1]] <<- data.frame(state=state, test="rddensity_jk", threshold=thr, year=scope,
    statistic=d$t_jk, p=d$p_jk, log_density_jump=d$logjump, ldj_ci_lo=d$lo, ldj_ci_hi=d$hi,
    MDD=d$mdd, N_left=d$Nl, N_right=d$Nr, stringsAsFactors=FALSE)
}

# ---- WA (pooled) ----
wa08 <- dens(wa$bac,0.08); wa15 <- dens(wa$bac,0.15)
adddens("WA","pooled",0.08,wa08); adddens("WA","pooled",0.15,wa15)
# ---- FL pooled (running = min of two samples) ----
fl08 <- dens(fl$run_min,0.08); fl15 <- dens(fl$run_min,0.15)
adddens("FL","pooled",0.08,fl08); adddens("FL","pooled",0.15,fl15)
# ---- FL by year ----
for (y in sort(unique(fl$year))) {
  sub <- fl$run_min[fl$year==y]
  for (cc in c(0.08,0.15)) {
    d <- tryCatch(dens(sub,cc), error=function(e) NULL)
    if (!is.null(d)) adddens("FL", as.character(y), cc, d)
  }
}
# ---- FL variant: sample1 only, pooled ----
fl08s1 <- dens(fl$run_s1,0.08); fl15s1 <- dens(fl$run_s1,0.15)
rows[[length(rows)+1]] <- data.frame(state="FL_sample1only",test="rddensity_jk",threshold=0.08,year="pooled",
  statistic=fl08s1$t_jk,p=fl08s1$p_jk,log_density_jump=fl08s1$logjump,ldj_ci_lo=fl08s1$lo,ldj_ci_hi=fl08s1$hi,MDD=fl08s1$mdd,N_left=fl08s1$Nl,N_right=fl08s1$Nr)
rows[[length(rows)+1]] <- data.frame(state="FL_sample1only",test="rddensity_jk",threshold=0.15,year="pooled",
  statistic=fl15s1$t_jk,p=fl15s1$p_jk,log_density_jump=fl15s1$logjump,ldj_ci_lo=fl15s1$lo,ldj_ci_hi=fl15s1$hi,MDD=fl15s1$mdd,N_left=fl15s1$Nl,N_right=fl15s1$Nr)

dens_df <- do.call(rbind, rows)

# ---- discrete binomial tests (both states, both thresholds, k grid) ----
drows <- list()
for (cfg in list(list("WA",wa$low_score), list("FL",fl$low_score))) {
  st <- cfg[[1]]; ls <- cfg[[2]]
  for (c0 in c(80,150)) for (k in c(1,2,5,10)) {
    r <- disc_test(ls,c0,k)
    drows[[length(drows)+1]] <- data.frame(state=st,test=paste0("discrete_binom_k",k),threshold=c0/1000,
      year="pooled",statistic=r$obs,p=r$p,log_density_jump=NA,ldj_ci_lo=NA,ldj_ci_hi=NA,MDD=NA,N_left=NA,N_right=NA)
  }
}
disc_df <- do.call(rbind, drows)

# ---- DCdensity (McCrary) WA from replication, for context ----
repl <- fromJSON("/workspace/eval/replication/codebase/outputs/density_tests.json")
mcrows <- rbind(
 data.frame(state="WA",test="DCdensity_McCrary_repl",threshold=0.08,year="pooled",statistic=repl$mccrary$thr_008$z,p=repl$mccrary$thr_008$pval,log_density_jump=repl$mccrary$thr_008$theta,ldj_ci_lo=NA,ldj_ci_hi=NA,MDD=NA,N_left=NA,N_right=NA),
 data.frame(state="WA",test="DCdensity_McCrary_repl",threshold=0.15,year="pooled",statistic=repl$mccrary$thr_015$z,p=repl$mccrary$thr_015$pval,log_density_jump=repl$mccrary$thr_015$theta,ldj_ci_lo=NA,ldj_ci_hi=NA,MDD=NA,N_left=NA,N_right=NA))

full <- rbind(dens_df, disc_df, mcrows)
write.csv(full, file.path(RES,"density_tests.csv"), row.names=FALSE)

# power verdict: FL MDD > 2x WA MDD?
pv <- data.frame(threshold=c(0.08,0.15),
  WA_MDD=c(wa08$mdd,wa15$mdd), FL_MDD=c(fl08$mdd,fl15$mdd),
  FL_p=c(fl08$p_jk,fl15$p_jk), WA_p=c(wa08$p_jk,wa15$p_jk),
  FL_over_2xWA=c(fl08$mdd>2*wa08$mdd, fl15$mdd>2*wa15$mdd))
write.csv(pv, file.path(RES,"florida_power.csv"), row.names=FALSE)
print(pv)
cat(sprintf("\nWA 0.08 rddensity p=%.3f logjump=%.3f MDD=%.3f | FL 0.08 p=%.3f logjump=%.3f MDD=%.3f\n",
  wa08$p_jk,wa08$logjump,wa08$mdd,fl08$p_jk,fl08$logjump,fl08$mdd))
cat(sprintf("WA 0.15 rddensity p=%.3f logjump=%.3f MDD=%.3f | FL 0.15 p=%.3f logjump=%.3f MDD=%.3f\n",
  wa15$p_jk,wa15$logjump,wa15$mdd,fl15$p_jk,fl15$logjump,fl15$mdd))
cat("\ndiscrete tests (FL):\n"); print(disc_df[disc_df$state=="FL",c("test","threshold","statistic","p")])
cat("wrote density_tests.csv, florida_power.csv\n")
