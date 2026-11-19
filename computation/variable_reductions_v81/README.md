# v81 variable-reduction package

The `abc` directory contains the complete 56-variable ordinary-abc
quartic: producer, quadratic specification, full coefficient table,
independent reconstruction, mathematical review and source pins.
It improves the v80 count of 58 by a nine-coordinate nonlinear contact
rechart. All counts include the input. Its arithmetic assumptions
and ineffective defining threshold are stated in the paper and review.

The retained elliptic chart and Laurent packing originate in **notes
of Gabe Conant with Astra 6.2**. The new changes are identified as
subsequent project work.

The `general` directory records a proved local scalar-detector lemma
and an exact homogeneous pole rechart. The full R²-free quadratic
compilation remains incomplete; it establishes no 164/179 count.

The related number-field work is in
`computation/number_fields/pasten_vidaux_v81`; those counts concern
the rational subfield inside a number field and do not replace any
Z-over-Q record.

Run `python -B scripts/verify_v81.py` from the repository root. The
default check is read-only; rebuilding coefficients is isolated in a
temporary directory by the gate.
