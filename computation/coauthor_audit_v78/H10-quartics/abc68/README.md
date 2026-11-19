# A 693-monomial quartic in 68 rational variables under ordinary abc

For every sufficiently large odd positive integer N, take the repository's shift B=N⁴. The coefficient table in `results/polynomial-scaled.json`, evaluated at N, has degree four, 693 monomials, primitive integer coefficients and height max(B+758542, 2B). In particular its height is 2B for odd N≥31. Its projection in the first coordinate is the integers under the assumptions of Brox's 68-variable theorem, including ordinary rational abc, its elliptic and prime-selection hypotheses, trace heights and simultaneous twists. The sufficient N for integer definition is ineffective. The extant 68-variable table has 1,078 monomials and height B²+1. All coordinate counts include the input.

The construction uses an invertible reference-coordinate change. Over Q(√2), set a=1+√2, c=4−2√2 and δ=−23+17√2. Replace the old reference variables u,w by S=v−c−au and T=aw−v+c. The reference equations become

    v(v+T−S)+δ = 0,
    ST+c(T−S)+2cv+2δ = 0.

Indeed the old unit row is the negative of the first row, and expanding (v−c−S)(v−c+T)=a and using δ=a−c² gives the second. The original samples use a row basis and a constant pivot. The verifier proves that the two reference row spaces with that pivot coincide. In the point-pair block replace the old h with μ−t. The other coordinates include the rational input unchanged.

Next apply the invertible row operations in the certificate and form the positive integer weighted sum of the 56 squared quadrics. An operation [i,j,n,d] uses zero-based row indices and replaces row i by the primitive normalization of d row_i + n row_j. The six nonunit weights are 272,368,391,391,2,2. The resulting unscaled polynomial is also supplied as a polynomial in B and has the same 693 coordinate monomials.

For the final table scale old coordinate i to N raised to its specified integer power times new coordinate i. Substitute B=N⁴ and divide each row by its smallest power of N. The input has exponent zero. The positive sum of squares remains equivalent for every positive N. The respective largest absolute coefficients at powers 0,1,2,3,4 of N in the expanded table are 758542,44,70,0,2. The only coordinate monomial that mixes powers is the constant B+758542. Some nonconstant coefficient has magnitude 2B, establishing the stated height.

Run `python check.py` alongside the `results` directory. Only the Python standard library is required. The independent checker pins the bundled upstream table by SHA-256 to the source at d3a8c223716a0fc0dbf5af4eb7998d640c21048d, checks the reference-row equivalence, applies every row and coordinate change, verifies both full expansions, and checks exact support, content and coefficient maxima.
