#!/usr/bin/env Rscript
# Panel A, part 2: A3 bandwidth curve, A4 sensitivity, A5 eras, A6 density, A7 balance.
.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))
suppressMessages({library(rdrobust); library(rddensity); library(RDHonest)
  library(fixest); library(dplyr); library(jsonlite)})
set.seed(1)
RES <- "/workspace/eval/followup/002-methods-and-transport/results"
df <- readRDS("/workspace/eval/replication/codebase/outputs/rd_data.rds")
df$DUIs <- as.integer(df$bac >= 0.08); df$DUIx <- as.integer(df$bac >= 0.081)
df$AGGs <- as.integer(df$bac >= 0.15); df$AGGx <- as.integer(df$bac >= 0.151)

specs <- list(
  s08  = list(thr=0.08, coding="statutory", cc=0.08,   c0=80,  tv="DUIs", cv="bac_c08"),
  s15s = list(thr=0.15, coding="statutory", cc=0.15,   c0=150, tv="AGGs", cv="bac_c15"),
  s15x = list(thr=0.15, coding="strict",    cc=0.1505, c0=150, tv="AGGx", cv="bac_c15"),
  s08x = list(thr=0.08, coding="strict",    cc=0.0805, c0=80,  tv="DUIx", cv="bac_c08")
)

############################# A3: bandwidth curve ############################
hgrid <- seq(0.010, 0.068, by=0.002)
a3 <- list()
for (nm in c("s08","s15s","s15x")) {
  s <- specs[[nm]]
  for (kern in c("uniform","triangular")) {   # rectangular == uniform in rdrobust
    for (hh in hgrid) {
      o <- tryCatch(rdrobust(df$recidivism, df$bac, c=s$cc, p=1, kernel=kern, h=hh,
                             vce="hc1", masspoints="adjust"), error=function(e) NULL)
      if (is.null(o)) next
      a3[[length(a3)+1]] <- data.frame(threshold=s$thr, coding=s$coding,
        kernel=ifelse(kern=="uniform","rectangular","triangular"), h=hh,
        est_conv=unname(o$coef[1]), se_conv=unname(o$se[1]),
        ci_rbc_lo=unname(o$ci["Robust",1]), ci_rbc_hi=unname(o$ci["Robust",2]),
        ci_conv_lo=unname(o$ci["Conventional",1]), ci_conv_hi=unname(o$ci["Conventional",2]),
        stringsAsFactors=FALSE)
    }
  }
}
a3 <- do.call(rbind, a3)
write.csv(a3, file.path(RES,"bandwidth_curve.csv"), row.names=FALSE)
cat("A3 bandwidth_curve.csv rows:", nrow(a3), "\n")

# sign-change + h* (first h where RBC CI excludes 0) per spec, triangular kernel
signinfo <- list()
for (nm in c("s08","s15s","s15x")) {
  s <- specs[[nm]]
  sub <- a3[a3$threshold==s$thr & a3$coding==s$coding & a3$kernel=="triangular",]
  sub <- sub[order(sub$h),]
  signs <- sign(sub$est_conv)
  changes <- any(signs != signs[1]) || (length(unique(signs[signs!=0]))>1)
  excl <- (sub$ci_rbc_lo>0) | (sub$ci_rbc_hi<0)
  hstar <- if (any(excl)) min(sub$h[excl]) else NA
  all_excl <- all(excl); none_excl <- !any(excl)
  signinfo[[nm]] <- list(threshold=s$thr, coding=s$coding, sign_change=changes,
    hstar_excl=hstar, all_excl=all_excl, none_excl=none_excl,
    min_est=min(sub$est_conv), max_est=max(sub$est_conv),
    hmin=min(sub$h), hmax=max(sub$h))
}
write_json(signinfo, file.path(RES,"_a3_signinfo.json"), auto_unbox=TRUE, pretty=TRUE, digits=6)
cat("A3 sign info:\n"); str(signinfo)

############################# A4: coding + donut sensitivity ################
donut_rd <- function(cc, c0, d) {
  keep <- abs(df$low_score - c0) > d
  dd <- df[keep,]
  o <- rdrobust(dd$recidivism, dd$bac, c=cc, p=1, kernel="triangular", bwselect="mserd",
                vce="hc1", masspoints="adjust")
  list(est=unname(o$coef[1]), se=unname(o$se[1]),
       lo=unname(o$ci["Robust",1]), hi=unname(o$ci["Robust",2]), h=o$bws[1,1])
}
a0_window <- function(tv, cv, lo, hi, controls) {
  dd <- df %>% filter(bac>=lo, bac<=hi)
  rhs <- sprintf("%s + %s + %s:%s", tv, cv, tv, cv)
  if (controls) rhs <- paste(rhs, "+ male + white + factor(aged) + factor(year)")
  m <- feols(as.formula(paste("recidivism ~", rhs)), data=dd, cluster=~low_score)
  ct <- coeftable(m)[tv,]
  list(est=unname(ct[1]), se=unname(ct[2]), lo=unname(ct[1]-1.96*ct[2]), hi=unname(ct[1]+1.96*ct[2]))
}
build_sens <- function(thrspecs, win05, win025) {
  rows <- list()
  for (sp in thrspecs) {
    s <- specs[[sp]]
    # (iii) with/without controls, A0 bw05
    a <- a0_window(s$tv, s$cv, win05[1], win05[2], TRUE)
    rows[[length(rows)+1]] <- data.frame(threshold=s$thr, coding=s$coding, variant="A0_bw05_controls", estimator="A0", est=a$est, se=a$se, ci_lo=a$lo, ci_hi=a$hi, h=0.05)
    a <- a0_window(s$tv, s$cv, win05[1], win05[2], FALSE)
    rows[[length(rows)+1]] <- data.frame(threshold=s$thr, coding=s$coding, variant="A0_bw05_nocontrols", estimator="A0", est=a$est, se=a$se, ci_lo=a$lo, ci_hi=a$hi, h=0.05)
    # (iv) A1 estimator, no donut
    d0 <- donut_rd(s$cc, s$c0, -1)  # d=-1 keeps all (abs>-1 always true)
    rows[[length(rows)+1]] <- data.frame(threshold=s$thr, coding=s$coding, variant="A1_nodonut", estimator="A1", est=d0$est, se=d0$se, ci_lo=d0$lo, ci_hi=d0$hi, h=d0$h)
    # (ii) donuts d in {0,1,2,3,5} (d=0 = drop single cutoff bin c0)
    for (d in c(0,1,2,3,5)) {
      dr <- donut_rd(s$cc, s$c0, d)
      rows[[length(rows)+1]] <- data.frame(threshold=s$thr, coding=s$coding, variant=paste0("A1_donut_d",d), estimator="A1", est=dr$est, se=dr$se, ci_lo=dr$lo, ci_hi=dr$hi, h=dr$h)
    }
  }
  do.call(rbind, rows)
}
sens15 <- build_sens(c("s15s","s15x"), c(0.10,0.20), c(0.125,0.175))
sens08 <- build_sens(c("s08","s08x"), c(0.03,0.13), c(0.055,0.105))
write.csv(sens15, file.path(RES,"sensitivity_015.csv"), row.names=FALSE)
write.csv(sens08, file.path(RES,"sensitivity_008.csv"), row.names=FALSE)
cat("A4 sensitivity_015.csv rows:", nrow(sens15), " sensitivity_008.csv rows:", nrow(sens08), "\n")

############################# A5: eras ######################################
era_rd <- function(dd, cc) {
  o <- tryCatch(rdrobust(dd$recidivism, dd$bac, c=cc, p=1, kernel="triangular", bwselect="mserd",
                vce="hc1", masspoints="adjust"), error=function(e) NULL)
  if (is.null(o)) return(list(est=NA,se=NA,lo=NA,hi=NA,n=nrow(dd)))
  list(est=unname(o$coef[1]), se=unname(o$se[1]), lo=unname(o$ci["Robust",1]), hi=unname(o$ci["Robust",2]), n=sum(o$N_h))
}
era_a0 <- function(dd, tv, cv, lo, hi) {
  d <- dd %>% filter(bac>=lo, bac<=hi)
  yfe <- if (length(unique(d$year))>1) "+ factor(year)" else ""
  m <- feols(as.formula(sprintf("recidivism ~ %s + %s + %s:%s + male + white + factor(aged) %s", tv,cv,tv,cv,yfe)), data=d, cluster=~low_score)
  ct <- coeftable(m)[tv,]; list(est=unname(ct[1]), se=unname(ct[2]), n=nobs(m))
}
erarows <- list(); pooled_for_fig <- list()
for (nm in c("s08","s15s")) {
  s <- specs[[nm]]
  win <- if (s$thr==0.08) c(0.03,0.13) else c(0.10,0.20)
  periods <- list(e1=1999:2003, e2=2004:2007)
  ests <- list()
  for (pn in names(periods)) {
    sub <- df[df$year %in% periods[[pn]],]
    a0 <- era_a0(sub, s$tv, s$cv, win[1], win[2]); a1 <- era_rd(sub, s$cc)
    ests[[pn]] <- a0
    erarows[[length(erarows)+1]] <- data.frame(threshold=s$thr, coding=s$coding, period=paste0(min(periods[[pn]]),"-",max(periods[[pn]])), estimator="A0", est=a0$est, se=a0$se, ci_lo=a0$est-1.96*a0$se, ci_hi=a0$est+1.96*a0$se, n=a0$n)
    erarows[[length(erarows)+1]] <- data.frame(threshold=s$thr, coding=s$coding, period=paste0(min(periods[[pn]]),"-",max(periods[[pn]])), estimator="A1", est=a1$est, se=a1$se, ci_lo=a1$lo, ci_hi=a1$hi, n=a1$n)
  }
  # era-difference test on A0 (Wald, independent subsamples)
  z <- (ests$e1$est - ests$e2$est) / sqrt(ests$e1$se^2 + ests$e2$se^2)
  pdiff <- 2*pnorm(-abs(z))
  erarows[[length(erarows)+1]] <- data.frame(threshold=s$thr, coding=s$coding, period="era_diff_1999-2003_vs_2004-2007", estimator="A0_diff", est=ests$e1$est-ests$e2$est, se=sqrt(ests$e1$se^2+ests$e2$se^2), ci_lo=NA, ci_hi=NA, n=NA)
  attr(erarows[[length(erarows)]], "z") <- z
  # year by year
  for (yr in 1999:2007) {
    sub <- df[df$year==yr,]
    a0 <- era_a0(sub, s$tv, s$cv, win[1], win[2])
    erarows[[length(erarows)+1]] <- data.frame(threshold=s$thr, coding=s$coding, period=as.character(yr), estimator="A0_year", est=a0$est, se=a0$se, ci_lo=a0$est-1.96*a0$se, ci_hi=a0$est+1.96*a0$se, n=a0$n)
  }
}
era <- do.call(rbind, erarows)
write.csv(era, file.path(RES,"eras.csv"), row.names=FALSE)
cat("A5 eras.csv rows:", nrow(era), "\n")

############################# A6: manipulation ##############################
# rddensity at both thresholds (pooled), p_jk
rdd_test <- function(cc) {
  r <- rddensity(df$bac, c=cc, massPoints=TRUE)
  s <- summary(r)
  jump <- r$hat$diff           # log? rddensity reports density diff; use test
  list(p_jk = r$test$p_jk, T_jk = r$test$t_jk,
       f_l = r$hat$left, f_r = r$hat$right,
       h_l = r$h$left, h_r = r$h$right, N_l=r$N$eff_left, N_r=r$N$eff_right)
}
rd08 <- rdd_test(0.08); rd15 <- rdd_test(0.15)

# discrete binomial test (spirit of Frandsen) over k adjacent bins each side
tab <- table(df$low_score)
cnt <- function(s){ v<-tab[as.character(s)]; if(is.na(v)) 0 else as.numeric(v) }
disc_test <- function(c0, k) {
  below_pos <- (c0-k):(c0-1); above_pos <- (c0+1):(c0+k)
  pos <- c(below_pos, above_pos); y <- sapply(pos, cnt)
  rel <- pos - c0
  fit <- lm(y ~ rel)                      # local linear fit excluding cutoff bin
  pred_c0 <- as.numeric(predict(fit, newdata=data.frame(rel=0)))
  obs_c0 <- cnt(c0)
  pred_c0 <- max(pred_c0, 1)
  n <- round(obs_c0 + pred_c0)
  p <- binom.test(obs_c0, n, p=0.5)$p.value   # obs vs smooth prediction
  list(k=k, obs_c0=obs_c0, pred_c0=pred_c0, p=p)
}
disc <- list()
for (c0 in c(80,150)) for (k in c(1,2,5,10)) {
  r <- disc_test(c0, k)
  disc[[length(disc)+1]] <- data.frame(threshold=c0/1000, k=k, obs_cutoff=r$obs_c0, pred_cutoff=round(r$pred_c0,1), p=r$p)
}
disc <- do.call(rbind, disc)

# replication DCdensity values from disk
repl <- fromJSON("/workspace/eval/replication/codebase/outputs/density_tests.json")

dens_rows <- rbind(
  data.frame(state="WA", test="rddensity_jk", threshold=0.08, year="pooled", statistic=rd08$T_jk, p=rd08$p_jk, log_density_jump=NA, ldj_ci_lo=NA, ldj_ci_hi=NA, MDD=NA),
  data.frame(state="WA", test="rddensity_jk", threshold=0.15, year="pooled", statistic=rd15$T_jk, p=rd15$p_jk, log_density_jump=NA, ldj_ci_lo=NA, ldj_ci_hi=NA, MDD=NA),
  data.frame(state="WA", test="DCdensity_McCrary_repl", threshold=0.08, year="pooled", statistic=repl$mccrary$thr_008$z, p=repl$mccrary$thr_008$pval, log_density_jump=repl$mccrary$thr_008$theta, ldj_ci_lo=NA, ldj_ci_hi=NA, MDD=NA),
  data.frame(state="WA", test="DCdensity_McCrary_repl", threshold=0.15, year="pooled", statistic=repl$mccrary$thr_015$z, p=repl$mccrary$thr_015$pval, log_density_jump=repl$mccrary$thr_015$theta, ldj_ci_lo=NA, ldj_ci_hi=NA, MDD=NA)
)
for (i in 1:nrow(disc)) dens_rows <- rbind(dens_rows, data.frame(state="WA", test=paste0("discrete_binom_k",disc$k[i]), threshold=disc$threshold[i], year="pooled", statistic=disc$obs_cutoff[i], p=disc$p[i], log_density_jump=NA, ldj_ci_lo=NA, ldj_ci_hi=NA, MDD=NA))
write.csv(dens_rows, file.path(RES,"density_tests_WA.csv"), row.names=FALSE)
write_json(list(rddensity=list(thr08=rd08, thr15=rd15), discrete=disc,
                replication_DCdensity=repl$mccrary, paper=repl$paper_reference),
           file.path(RES,"_density_WA.json"), auto_unbox=TRUE, pretty=TRUE, digits=6)
cat("A6 density done. rddensity p: 0.08=",round(rd08$p_jk,4)," 0.15=",round(rd15$p_jk,4),"\n")
print(disc)

# rdplotdensity figures for WA (ggplot objects; save separately, never block A7)
tryCatch({
  suppressMessages(library(ggplot2))
  for (cc in c(0.08,0.15)) {
    r <- rddensity(df$bac, c=cc, massPoints=TRUE)
    p <- rdplotdensity(r, df$bac, plotRange=c(cc-0.05, cc+0.05),
                       histBreaks=seq(cc-0.05,cc+0.05,0.002), plot=FALSE)$Estplot +
         ggtitle(sprintf("WA BAC density at %.2f (rddensity p=%.3f)", cc, r$test$p_jk))
    ggsave(file.path(RES, sprintf("fig_density_WA_%03d.png", round(cc*1000))), p, width=6, height=4, dpi=140)
  }
}, error=function(e) cat("density fig skipped:", conditionMessage(e), "\n"))

############################# A7: covariate balance (A1) ####################
bal_rd <- function(y, cc) {
  o <- rdrobust(df[[y]], df$bac, c=cc, p=1, kernel="triangular", bwselect="mserd", vce="hc1", masspoints="adjust")
  data.frame(covariate=y, threshold=ifelse(cc<0.1,0.08,0.15), est=unname(o$coef[1]), se=unname(o$se[1]),
             ci_rbc_lo=unname(o$ci["Robust",1]), ci_rbc_hi=unname(o$ci["Robust",2]), p_rbc=unname(o$pv["Robust",1]), h=o$bws[1,1])
}
bal <- do.call(rbind, lapply(c("male","white","aged","acc"), function(y) rbind(bal_rd(y,0.08), bal_rd(y,0.15))))
write.csv(bal, file.path(RES,"balance_A1.csv"), row.names=FALSE)
cat("A7 balance done.\n"); print(bal[,c("covariate","threshold","est","se","ci_rbc_lo","ci_rbc_hi","p_rbc")])
cat("\nPanel A part 2 complete.\n")
