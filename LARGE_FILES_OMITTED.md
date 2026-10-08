# Files omitted from this repository

Nothing produced by the replication or the extension studies was cut for size. The items below
were left out because they are third-party software or staged copies of public inputs, not part of
the runs themselves.

| Omitted | Size | Provenance / how to recreate |
|---|---|---|
| `followup/002-methods-and-transport/workspace/.venv/` | ~165 MB | Python 3.12 virtual environment (pandas, pyarrow, matplotlib, numpy, Pillow, fontTools). Recreate with `pip install pandas pyarrow matplotlib`. |
| `followup/002-methods-and-transport/workspace/rlib/` | ~2.2 MB | Installed CRAN packages `rddensity`, `lpdensity`, `RDHonest` (also used by 004). Recreate with `install.packages(c("rddensity","lpdensity","RDHonest"))`. |
| `shared-data/` staging mirror | ~24 MB | Public inputs: FDLE STED index page, FDLE memo and 2022 statistics sheet; Utah CCJJ DUI annual reports (FY2018–FY2025) and derived arrests-by-BAC CSV; NHTSA Traffic Tech DOT-HS-813-234; literature table and five source working papers. Each study's report lists the paths and sha256s it used. |
| FDLE STED PDFs | n/a | Never stored: downloaded from www.fdle.state.fl.us, parsed in memory and deleted file by file (they contain names). URLs and sha256s are in `fl_manifest.csv`. |
| openICPSR 112907 do-files | < 1 MB | Login-gated, code-only author deposit (doi:10.3886/E112907V1); not obtained. |
