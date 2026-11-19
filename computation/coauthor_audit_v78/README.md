# Coauthor audit and extensions, v78

This package integrates the two coauthor archives supplied on 19 November 2026,
with separate independent audits and further proved improvements. Their original
attribution is retained. See the complete [result guide](../../docs/results_20261119_v78.md)
and [result table](../../data/results_20261119_v78.json).

`H10-quartics` and `H10-eleven-variables` contain the new material from those
archives. Their duplicated upstream sources are recorded in `source_bindings.json`
and materialized from the pinned repository files. `ORIGINAL_SHA256SUMS` preserves
the archive checksum lists, including the original PDFs that are not duplicated
in this source publication. Those complete lists were verified before extraction
and integration. They are provenance records, not checksum commands for this
deliberately deduplicated layout.

The new work is in four separate directories:

- `work_general`: shared-factor audit, strengthened extraction, enhanced 165-variable
  table, and the explicit 108-bit 180-variable quartic.
- `work_abc`: constant-free 62-variable gates, coefficient normalization, weaker
  fixed-exponent hypotheses, and the 63/64/67-variable extensions.
- `work_root`: four-contact scalar and 25/27-variable degree improvements; the
  first-scale twelve-contact ordinary-abc eleven-variable construction.
- `work_weak11`: enlarged auxiliary charts, ordered guard removal, improved
  weak-abc eleven-variable bounds, and independent ancillary certificates.

The directory labels identify the separate audit workstreams; all contributions
belong to the project under the repository's attribution and license terms.
The original coauthor reductions are credited in every associated proof.

Run from the repository root:

```sh
python3 -B scripts/verify_v78.py --report /tmp/v78.json
```

This constructs the original expected layout in a temporary directory and runs
all original and new finite checks, without changing the checkout. The
independent checkers do not import the corresponding new producers. They do
reuse explicitly pinned, independently checked source chart and norm interfaces
where stated. The arithmetic premises and universal arguments are in the six
papers listed by `paper_paths.json`.

To obtain a directly runnable offline layout, use
`python3 -B scripts/verify_v78.py --materialize /tmp/v78-offline`.

The best-count claims proved here are 165, 180, 62 and 11, including the input.
No result here proves the open 21/9 physical realization requirements or a global
minimum. All small family fixtures and coefficient-height crossover thresholds
are distinguished from sufficient defining parameters.
