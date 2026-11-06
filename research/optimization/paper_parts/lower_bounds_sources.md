# Lower-bound sources and audit notes

## Results

* For every number field K, a single polynomial F(T,Y_1,...,Y_r) defining O_K in K requires r>=2 and total degree>=4. These are unconditional obstructions: they do not assume the repository proof.
* Stronger (using Siegel): a one-witness rational projection contained in O_K must be finite; likewise any projection of a polynomial of total degree at most three contained in O_K must be finite.
* This proves degree optimality of any valid quartic Z-in-Q construction, independently of variable count. It does not prove 3 total variables possible.
* No priority/novelty claim is made; these are deductions from classical results with cone/reducibility details written out.

## Primary sources inspected

1. Janos Kollar, *Unirationality of Cubic Hypersurfaces*, J. Inst. Math. Jussieu 1(3) (2002), 467--476. DOI https://doi.org/10.1017/S1474748002000117. Original author preprint https://arxiv.org/pdf/math/0005146 (submitted May15,2000). Theorem2 on page1 was read directly: perfect field; irreducible cubic hypersurface dimension>=2; not a cone over an (n-1)-dimensional cubic. Unirational, having a rational point, having a smooth rational point are equivalent. The manuscript lower bound retains the cone exclusion and uses K=number field (perfect, characteristiczero). Cambridge publisher metadata independently verifies publication details. Web refs turn11view0, turn14view0, turn34search0.
2. Andrzej Schinzel, *Polynomials with Special Regard to Reducibility*, Encyclopedia Math.Appl.77, Cambridge2000, DOI https://doi.org/10.1017/CBO9780511542916. Publisher excerpt https://assets.cambridge.org/97805216/62253/excerpt/9780521662253_excerpt.pdf was read. Introduction page5 explicitly states infinitely many integer specializations and explains root-solvability for sufficiently many integers implies rational-function solvability. Chapter4Section4 is the Hilbert theorem section, from the introduction. Exact formal theorem number inside full book not claimed. Webrefs turn25view0,turn31search2.
3. Peter Mueller, *Finiteness Results for Hilbert's Irreducibility Theorem*, arXiv math/0109071 (2001), https://arxiv.org/pdf/math/0109071. Introduction explicitly states integral specializations over O_K; Section2.1 carries out integral-coordinate/Siegel reduction. No invented journal venue. Webrefs turn28academia22,turn30view1.
4. Serge Lang, *Fundamentals of Diophantine Geometry*, Springer1983, DOI https://doi.org/10.1007/978-1-4757-1810-2. Chapter8, *Siegel's Theorem and Integral Points*, pages188--224, DOI https://doi.org/10.1007/978-1-4757-1810-2_8. Publisher metadata and chapter title verified; general rational-function formulation corroborated by Mueller's cited use and other standard sources. Webrefs turn34search2--4. The optional strengthening is the only part needing Siegel; main r>=2,deg>=4 theorem does not.

## Edge cases checked in proof

* Total degree includes distinguished input. Number of witnesses excludes it.
* Zero polynomial defines allK; nonzero constants empty. Zero-witness nonzero polynomial finite.
* Integral Hilbert irreducibility, not just K Hilbertian, is needed. All specialization denominators and leading coefficients included in finite forbidden set.
* A linear factor over K(T) gives rational root for cofinite K, even if it originally comes from a nonmonic polynomial.
* Over arbitrary numberfields use complete Minkowski product; O_K need not be discrete in a single embedding.
* Cubic cone vertex is kernel of a rational linear map v->D_vH, so a geometric cone has rational vertex directions in characteristiczero. Quotient removes all vertices.
* Cone lines preserving integral-only input force vertex to annihilate BOTH homogenizing and input coordinates. This preserves exact affine input projection after quotient, including lifts by linear splitting.
* Reducible degree<=3 has only degree1/2 factors; each integral-only projection finite. Irreducible cubic homogenization stays irreducible.
* Quotientdim1 handled by one-witness theorem, not mistaken unirationality of genusone curves; dim0 finite.
* A system of quadratics is not ruledout; a single sumofsquares equation has degree4.

## Files

lower_bounds.tex is an includable section (no preamble), about340lines. lower_bounds.bib has separate citation keys prefixed lb. Main theorem can be integrated as unconditional. Optional last subsection uses Siegel for the stronger finiteness statement.

## Second audit: geometric irreducibility

The proof now handles this independently of Kollar's convention. An irreducible cubic over a characteristic-zero field that is geometrically reducible is a product of three distinct conjugate linear forms. Every Kpoint lies on all three hyperplanes. Two Kpoints with different affine input values then give a full rational line and every input in K. This excludes the case before invoking Kollar, whose quoted version is now restricted to geometrically integral cubics. Quotient by the vertex preserves geometric integrality. Thus nonsplit hyperplane unions, even with all rational points singular, present no gap.
