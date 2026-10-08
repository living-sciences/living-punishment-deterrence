# data/ — keyless deposits

## mixtape/hansen_dwi.dta  (9.45 MB, sha256 08158875811feeac8b4b92604efc1a90f5f2b8181144c2880c0f4fb60743ecd1)
Source: https://raw.githubusercontent.com/scunning1975/mixtape/master/hansen_dwi.dta
(Scott Cunningham, "Causal Inference: The Mixtape" companion repo, commit 6c8ca0fa, 2022-01-02;
identical bytes in github.com/scottcohn97/hansen2015_RDD_replication/Data/). Accessed 2026-10-05.
Per the Mixtape RD chapter (https://mixtape.scunning.com/06-regression_discontinuity), this is a
SUBSET of Hansen's data that Hansen gave Cunningham: 214,558 tests vs the paper's 512,964.
Variables (12): Date (1999-01-02..2007-12-31), Alcohol1, Alcohol2 (BAC x1000, two readings),
low_score (= min of the two; the paper's running variable), bac1, bac2 (/1000), male, white,
aged (21-80), year, acc (accident at scene), recidivism (4-yr window).
MISSING vs paper: county, prior-test count / prior-offense flag, PBT, recidivism-type splits,
alternate windows, court outcomes (Table 7), other-crime outcomes (Table 9), person ID.
De-identified; no names/IDs. Never attempt re-identification.
