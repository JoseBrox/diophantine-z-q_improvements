# Eight certified source integers (v141)

This is a genuine source reduction, not a quotient-certificate renaming. It uses the binomial coding theorem of BDHMS, arXiv:2506.20909v3, Theorem 1, Lemma 2.7 and Definitions 1.5, 1.7, 2.1, 2.3, rather than the original Jones prefix. It is an alternative to v139, not an improved total-variable record. The v139 arithmetic premises are retained.

## Coding prefix with two integer inputs

Start with an instance-specialized natural-number polynomial P in nu<=58 variables of degree delta<=4 (the classical universal pair (58,4)). If P(0)=0 return the yes quartic v^4; a nonzero constant gives the no quartic 1+v^4. Otherwise negate P if necessary so its constant term is positive. This is a suitable coding polynomial with the formal instance parameter zero. Set d=delta+1; let beta be the smallest power of 4 exceeding 2 delta! ||P||_1 (nu+2)^delta.

The only independently certified prefix inputs are f,g. Define b=1+3f, B=beta b^delta, H_i=B^(d^i) (0<=i<=nu+1), and

    N0=B H_nu, N1=4 B H_nu^(2 delta+1), N=N0 N1,
    mu=b H_nu, mask=N0-1-(b-1) sum_{i=1..nu} H_i.
    Ccoeff=H_(nu+1) sum_I P_I I! (delta-|I|)! prod_j H_j^(-I_j).
    G0=(N1/4-1)/(B-1),
    K=(1+g)^delta Ccoeff+B G0/2,
    S=g+2 K N0, T=mask+(B-2) H_(nu+1) N0,
    R=(S+T+1)N+T+1, r=(N-1)R, M=N^2.

These are the BDHMS radix prefix at instance parameter zero. The exponents of B in Ccoeff are nonnegative. G0 is an integral finite geometric sum and B is even. Thus once f,g are integers and f>=1 all helpers are integers. In particular these are not additional certified inputs. Impose f>=1 and (g-1)(2mu-1-g)>=0 by ternary triangular equations 2A=sum_{j=1}^3 t_j(t_j+1); for integral A, the lower bound -3/4 proves soundness, and Gauss's theorem gives completeness. Consequently b>=4 and 1<=g<2mu. Theorem 1 identifies solvability of P with b a power of two and M dividing binom(2r,r); for completeness one may take b=4^e arbitrarily large, f=(b-1)/3 and g>=b. The prefix is built from the published theorem, not the nine-input universal polynomial.

## Six remaining integers

Use w,s,h,gamma,j,i_half from the v128 signed binomial core (24 rows, with the old power_C^2 term removed from the margin). The original Jones power q=b^(5^60) and its quotient roles do not occur. The radix ladder of this alternate prefix is a separate cost.

The guarded linear targets force w,s nonzero; use direct targets for all eight except i_half+1. Since b=1 mod 3 and beta is a power of 4, B,H_i,N0,N1,N are 1 mod 3, hence 3|r. Also r>=3b by BDHMS Lemma 2.7, M>=b^4>=4b and M>=16. Thus 3 divides the first Pell parameter (wM+1)r(sM). The integral shifted trace and half-trace equation give c,d integral by v106. The unstrengthened margin yields |c/k-sM|<1/2, with k nonzero. The small congruence gives |k|>=r+1 and |c|>2r+1. Use i=2i_half+1, automatically nonzero. The v95 third-Pell theorem identifies |c|=Y_(2r+1)(|a_Pell|), and the small Pell norm and congruence identify |k|=Y_(r+1)(|p|). The signed trace/ratio and alternating truncation argument of v101 (after its nonzero exclusion) applies using r>=1, M>=16, M>=4b and the unstrengthened margin. It yields |bw|=2^(2r+1) and M|binom(2r,r). The extra size assumptions in v101 for recovering the original q are unnecessary here. This proves soundness.

For completeness choose canonical positive binomial witnesses, with the second Pell index an odd multiple of (2r+1)c: odd c implies odd i, and the index can be chosen so i>1. The v95 positive j and v106 half-trace witnesses exist. All direct targets are nonzero, as is i_half+1. Thus precisely eight integers are certified: f,g,w,s,h,gamma,j,i_half.

## Compilation and scope

build.mjs is a uniform compiler for any supplied instance-specialized quartic natural-number polynomial in at most 58 variables. It constructs quadratic radix rows and shares inverse products of degree two in the coefficient evaluation, then composes with the v139 comparison interface. For degree four the source uses 4nu+68+p2 variables, where p2 counts distinct shared pair products and p2<=nu(nu+1)/2. Lower degrees require no greater bound. This gives at most 2011 source variables, including all eight inputs, and 14 fewer source rows. The elliptic transfer adds 423/443 variables and 372/390 rows in the general/specified routes.

The comparison aggregate now has eleven finite points and 44 Boolean failures, within the v139 exclusion p<=60. The weighted height theorem applies for this fixed cardinality, with effective bounds enlarged to the fifteen-point ones if needed. The v136 recursive scalar proof applies with eight targets, keeping the larger square multiplier of v139; the dyadic depth and squareclass preparation are unchanged and the real lower bound is at least the previous bound. Hence the retained arithmetic premises suffice.

Uniform quartic upper bounds: 2434/2454 rational variables and 2369/2387 quadratic rows, not competitive with the v139 preferred bounds 622/642. No new unconditional undecidability theorem is asserted. We have not instantiated a fixed concrete universal quartic or run full CI. The verifier checks twelve exact rational prefix fixtures against the direct radix formulas and six actual table builds, including a sparse 58-variable test polynomial (725/745 variables, not a universal instance). These are compiler checks, not tests of undecidability. Run verify.mjs with Node from the repository root; see the compiler for the input format. The next task is to compress or replace the expensive radix/coefficient circuit while retaining the reduced number of certified source integers.
