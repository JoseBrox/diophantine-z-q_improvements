# External candidate: the upstream explicit 250-variable quartic

Status: primary source inspected; arithmetic and complete expansion not independently reproduced in this session. No certified result in the improvements repository is replaced by this note.

Upstream repository: elliotglazer/diophantine-z-q.
Read-only source pin: commit 498efba6fe75e9d28d6804f1391d7f70e4150afa, tree 0d27b011d1f29981d09c5b31b058ea962fb14397, 17 November 2026.
Primary release description:
https://github.com/elliotglazer/diophantine-z-q/blob/498efba6fe75e9d28d6804f1391d7f70e4150afa/research/version19/README.md

The release attributes the explicit quartic to Gemini Carbon and uses Brox's construction as its arithmetic foundation. It reports N=10220, 250 variables including the input, 222 quadratic residuals, and 3,362 nonzero monomials. The stated exact largest coefficient is
149^898+1747145497790223592810060471184416344603224790540808983,
which is below 2^6483.

Relevant files at the same commit:
- manuscripts/quartic_v19.tex
- research/version19/DEPENDENCIES.md
- research/version19/construction/check.py
- research/version19/construction/plain-text/quartic250-decimal.txt
- research/version19/construction/coefficients/quartic250-decimal.json

Reported TeX identity: git blob 319f15ca61f607e7e504a65f7a8bef984342c664; SHA256 1f0e4db9e978115bb7f605f4bfcd84426a715b8cb6adaee3566107b33d61ad03. The plain expression is reported as 85,737 bytes. These particular hash/byte metadata were reported by the independently inspecting research agent; the root reopened and verified the pinned release description.

The next integration requires reproducing the exact expansion and checking the reflected ten-contact height bound, its explicit constants, and its relation to the retained five-contact supplier. A finite expansion check alone is not an arithmetic proof. The current certified explicit 257-variable record remains unchanged until that audit is completed.

This candidate does not improve the general 25-variable, weak-abc 13-variable, ordinary-abc 11-variable or ordinary-abc quartic 71-variable records. No upstream repository was modified.
