# v148: shared small/third Pell congruence core, and its remaining obstruction

**Subsequent status (v151):** the [global counterexample theorem](../shared_pell_global_obstruction_v151/README.md) disproves the shared-sum integrality implication even on false packed prefixes. The conditional index theorem below, with integral ordinates, remains valid.

This is a **partial source result**, not a seven-integer undecidability transfer. The eight certificates of v147 remain in its actual compiler. The construction below changes the small Pell parameter and the second-norm quotient, so the old binomial-rounding and exceptional-fiber arguments cannot simply be quoted for it.

## 1. Coprime-modulus index theorem conditional on two integral ordinates

Use the signed polynomial Pell sequences X_n(A),Y_n(A) of v95. Let M be a positive even integer with M>=16, r>=1, B=2r+1, M²>3r+2. Let nonzero signed integers w,s be given and set U=wM, Y=sM, a=(U+1)rY, P=1+2Ur²Y². In particular a is divisible by M, P=1 modulo M², |a|>=2 and |P|>|a|. The last inequality follows from |U|>=M and |Y|>=M.

Assume integers c,d satisfy the first norm d²-(a²-1)c²=1 and the retained halftrace square zeta²=2(ad+(a²-1)c+1) with rational zeta. Suppose a nonzero integer i' is available and

    F²-(a²-1)(M i' c²)²=1,
    G=a+F²(c+1-a),
    k=r+1+M² h,
    H=c+F²(B-c)+cF j,
    tau²-(P²-1)k²=1,
    I²-(G²-1)H²=1,
    k²>4(c-kY)²,
    h+j=L in Z.

The **additional assumption in this theorem** is that k and H are integers; h,j,F,tau,I,zeta may initially be rational. Then both h,j are integers, and the exact absolute Pell indices satisfy

    |c|=Y_B(|a|),  |d|=X_B(|a|),
    |k|=Y_(r+1)(|P|),  |tau|=X_(r+1)(|P|).

Proof. The rational square zeta² is an integer, so zeta is an integer. As a is even, even c would give zeta²=2 modulo 4. Thus c is odd. Integral first-norm classification writes |c|=Y_t(|a|), with odd t (the recurrence modulo 2 gives Y_t(A)=t modulo 2). The recurrence modulo M has parameter |a|=0 and gives Y_t(|a|)=(-1)^((t-1)/2) modulo M, so gcd(c,M)=1. The second norm makes F integral and F²=1 modulo M, giving gcd(F,M)=1 and hence gcd(M²,cF)=1.

By the assumed integrality of k,H, the reduced denominators of h,j divide M² and |cF| respectively. As h+j is integral, these denominators are equal; the coprimality forces denominator one for both. This is a literal single common quotient certificate in the integral-ordinate setting.

The congruence k=r+1 modulo M² implies |k|>=r+1, since M²>2(r+1). The margin gives |c|>(|Y|-1/2)|k|>B. Apply the signed v95 third-norm theorem with i=M i', which is a nonzero integer: this gives the claimed first index B and |G|>=2. Also |k|<|c| from the margin. Integral small-norm classification gives k=epsilon Y_l(P) for some l>=1 and sign epsilon, since P may be negative but the signed polynomial sequences cover both signs. Because |P|>|a| and Y_l(A) is increasing in l and nondecreasing in A>=2, l<B. (For l>=B it would exceed |c|.) Reducing the recurrence modulo M² gives epsilon l=r+1 modulo M², since P=1 modulo M². The bound M²>3r+2 and 1<=l<B exclude any other congruence, including the negative-sign branch. Therefore l=r+1. The norms recover the asserted absolute traces. No positivity of rational h or j was assumed.

Positive *norm/congruence* completeness for canonical c=Y_B(a),d=X_B(a) with a,P positive follows as well, separately from the margin: choose a sufficiently large positive multiple q of the order of the norm-one Pell unit matrix modulo M c². Then Y_q(a) is divisible by M c², so i'=Y_q(a)/(M c²)>0 and F=X_q(a) satisfy the modified second norm. The v95 positive third-congruence construction gives integral positive j with H,I positive. For the small norm use k=Y_(r+1)(P), tau=X_(r+1)(P); the recurrence modulo M² gives integral h, which is positive because r+1>=2 and P is sufficiently large (indeed P>=1+2M³). Set L=h+j. The first halftrace is the standard square at half-index (B+1)/2. This proves simultaneous canonical congruence witnesses, not the original margin/binomial equivalence for P instead of p.

## 2. Why a genuinely rational merger still needs a new idea

For fixed nondegenerate data, put k=k0+A h, H=H0+B0 j with A,B0 nonzero integers, and discriminants D1=P²-1,D2=G²-1 both nonzero. Let alpha h+beta j+gamma be any fixed rational affine combination with alpha,beta nonzero. Choose an odd prime ell splitting both quadratic discriminants and avoiding the finitely many coefficient numerators/denominators and discriminant primes. Such primes exist, for example by choosing primes 1 modulo a suitable common modulus and quadratic reciprocity.

For any n>=1 and a fixed integer L, take

    h=ell^(-n),
    j=(L-gamma-alpha*h)/beta.

Both h,j and both k,H have valuation -n at ell. The two norms are solvable in Q_ell: D1 and D2 are square units, and
1+D1 k²=D1 k²(1+1/(D1 k²)), with the parenthetical factor a square by Hensel; likewise for H. Yet the certified affine combination is exactly the integer L. This holds even if gcd(A,B0)=1. It applies both to the original and redesigned congruences. It proves a local obstruction to deducing separate integrality from the two rational norms and a single fixed affine combination, even with coprime moduli. It does **not** assert the existence of global rational false witnesses for every merger, or rule out a different source design.

## 3. Status and next step

The redesigned moduli isolate the two quotient denominators at the integral-ordinate stage and preserve exact signed absolute indices there. Unlike the v146 discussion, the coprimality is proved from the even packed parameter, the first halftrace, and a changed second norm. But the two integral-ordinate hypotheses are not consequences of the rational norm system and common quotient. They must be obtained jointly without adding back two separate integrality predicates. A successful rational completion must also reprove the strict binomial-margin and signed power-of-two reconstruction for P=p+1 and the modified second norm, including all exceptional fibers and complete canonical witnesses. No new source count is asserted. The local lemma is a rigorous restriction on simple affine mergers, not a lower bound on the optimal number of integer predicates.
