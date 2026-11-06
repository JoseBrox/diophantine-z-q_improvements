# Importing the complete research checkpoint

The full repository archive is named **diophantine-z-q_improvements_complete_20261106.zip** (approximately 17.5 MB). It contains 424 files in their intended repository-relative locations: all 414 files in the supplied research archive, a separately navigable copy of the final paper, a didactic README, benchmarks, verification scripts, and a small GitHub Actions workflow.

The GitHub connector has published the paper and comparison index. Its current upload operations accept content strings, not the large, binary ZIP or its contained GZIP certificates. **The research and certificate directories therefore have not yet been imported to GitHub.**

## Import without losing history

Download the complete ZIP from the accompanying ChatGPT answer, then run these commands **on your own computer** (substitute the ZIP download directory):

~~~sh
git clone https://github.com/JoseBrox/diophantine-z-q_improvements.git
cd diophantine-z-q_improvements
python3 -m zipfile -e /path/to/diophantine-z-q_improvements_complete_20261106.zip .
python3 scripts/check_archive_integrity.py
python3 scripts/report_benchmarks.py
git status
git add -A
git commit -m "Import complete checked research archive and reproducibility files"
git push origin main
~~~

The archive contains a complete README of its own, which will replace the interim online README when extracted. It also contains the full raw and GZIP data with original paths and bytes. Keep the original source files unmodified to preserve SHA-256 receipts.

If git push fails because of branch changes, fetch and merge the current upstream branch rather than force-pushing. The first verification command must say **PASS** before committing; a SHA-256 mismatch means the source archive did not unpack correctly.

## What the archive checks

The included historical MANIFEST.json records SHA-256 checksums and byte lengths for 412 immutable source files, while the original ZIP also holds MANIFEST.json and README.txt. The new script checks these 412 files, the separate paper copy, and the six comparison rows. This is an **integrity** test, not a certification of the mathematical arithmetic assumptions.

The old research/phase3/verification_index.py is a historic checker whose code deliberately asserts the upstream **git revision** and original root layout. It should be rerun in a matching upstream source checkout, not silently in this new GitHub repository.

## Publication cautions

Some certificates and scripts are for comparison cases or record known obstructions. Their presence does not assert that every candidate defines Z in Q, nor that the proposed number-field analogues are correct. See the manuscript for exact hypotheses, proofs, and counterexamples.