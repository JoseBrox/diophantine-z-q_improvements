# Structural alternatives to the 204-variable construction

This note records local obstructions and an uncompleted possible reduction. It does not claim a new defining polynomial. The baseline is Jose Brox's repository at d337a5500e2531139445bd7e30f966f62c4db03a, particularly `quartic204_20261114_v27.tex`.

## 1. Merging the two additive contact weights by multiplication

Let

R(t)=P_5((t-1)^2)/(t-1)^10.

The exact symmetry is R(2-t)=R(t). For any sufficiently large rational T, put lambda=1-T/2. Then lambda+T=2-lambda and

R(lambda)R(lambda+T)=R(lambda)^2.

Thus the odd-valuation radical of the product is 1, regardless of the heights of T and lambda. Both weights R(lambda),R(lambda+T) lie in (0,1) once (T/2)^2 exceeds the largest squared contact distance (namely 4). Consequently both contact q values are positive. Positivity of the weights therefore does not remove this obstruction. The assertion is an obstruction to recovering the old height estimate from the odd radical of a product. It is not a construction of a spurious solution of all the 204-variable equations.

The repository already contains more general product and rational-combination obstructions for predecessor constructions; this is their direct specialization to the current additive geometry.

## 2. Eliminating the second integral Lucas coordinate by monicity

For integers a,t and rational w, suppose

(a-2)^2 t^2 - a(a-2)t w + w^2 = 1.

As a polynomial in w this is monic with integer coefficients. Hence w is an integer. If a>=3 and t is nonzero, the integer coordinate x=(a-2)t is divisible by a-2. The usual classification of Pell norm-one solutions then forces an index of size at least a-2, apart from the small boundary cases handled in the source. Thus at the level of exact integer equations it is possible to use two integer labels a,t and one rational witness w rather than three integer labels.

This does not yet eliminate an elliptic point in the quartic construction. The stored quantities L2,L3 are approximate formal ratios, not the exact integer labels a,t. The old argument proves the integer residual Delta is zero using a polynomial-in-B bound on its absolute value. An arbitrary rational w has no such height bound, and its denominator prevents the same residual argument. Treating the rational-root theorem as applicable before Delta=0 is circular. A valid use of this observation would require a new height control for w or an exact algebraic coupling of the index values.

## 3. Setting the Pell coefficient equal to beta does not force integrality

Take

X=1/357,
beta=51X^2+2504=6257497/2499,
b=1251499,
t=3133753497=2504b+1.

Then gcd(t,b)=1 and

t^2-beta*t*b+b^2=1,

but X is not an integer. Hence even coprime integral Pell coordinates do not make this rational coefficient integral. This prevents a particularly simple attempt to delete the separate scalar index and use beta directly as the norm-form parameter.

The example follows from v=357,u=1 and

127704u^2-v^2=255,
(2504v^2-51u^2)/255=1251499.

## 4. A limitation of eliminating every auxiliary from the growth relation

Let F(A,T) be a nonzero polynomial in Z[A,T]. For every integer a for which F(a,T) is nonzero, any integer root t has |t| bounded by a fixed polynomial in 1+|a|. Indeed, write F(a,T)=sum c_i(a)T^i and apply the Cauchy root bound; its nonzero leading coefficient is a nonzero integer, hence has absolute value at least 1. Therefore log|t|=O(log|a|).

It follows that a construction requiring log B to grow like |a| log|a| cannot retain only one additional integer label satisfying a fixed nonzero algebraic equation F(a,t)=0. This does not rule out existential rational auxiliaries, whose arithmetic may be essential, or other kinds of growth amplification.

## 5. Adding a free square to the trace

The proposal lambda=T+r^2 would permit an extra free rational variable for prime selection but needs a new estimate controlling all elliptic indices by h(lambda) alone. The available family theorem only yields a bound involving h(r) as an additional parameter height. Positivity does not in general remove this term: the rational unit circle u^2+r^2=1 has unbounded rational coordinate heights.

For a single elliptic abscissa, the corresponding curve is

y^2=(lambda-r^2)^3-D(lambda-r^2),

a genus-two family at generic lambda. Uniformly bounding the elliptic index by h(lambda) is a further family-height assertion, not a consequence of the fixed-abelian theorem quoted in the baseline. No proof under the inherited premises is provided here.

## 6. Eliminating the input point through a shifted Pell coordinate

Another proposal is

w=(a-2)b+beta,
Delta_beta=t^2-a*t*w+w^2-1,

with integral labels a,t,b. If Delta_beta=0, the rational-root theorem applied to the monic polynomial in w makes w, and hence beta, integral. Completeness at the exact Pell-equation level can arrange a Lucas index congruent to beta modulo a-2.

The missing step is proving Delta_beta=0. Writing beta=u/v in lowest terms, its reduced denominator divides v^2, and the numerator has a bound of the shape

|num(Delta_beta)| <= C B^4 exp(2h(beta)),

with a harmless enlargement of C and of the exponent of B if one changes the convention for B. The order-three contact comparison therefore yields only a bound log B <= C' h(beta)+C'', not the original polynomial contradiction. The scalar bound h(beta)<=epsilon_N a(1+log a/3) is compatible with this for arbitrarily large a: the numerical choices B=a and h(beta)=sqrt(a) demonstrate the lack of a contradiction for every fixed positive epsilon_N. This observation concerns the available inequalities, not existence of actual full witnesses.

Pell growth and continued-fraction classification apply only after exact vanishing; using them to prove vanishing here is circular. At a prime dividing the denominator of beta the dominant beta^2 term of Delta_beta has negative even valuation. The original negative-odd pole obstruction therefore does not by itself make Delta_beta integral. More fixed contact blocks can improve a power-type scalar estimate h(beta)<<a^delta, but do not supply the logarithmic estimate h(beta)<<log a that would absorb the denominator loss. No valid repair under the inherited estimates has been obtained.
