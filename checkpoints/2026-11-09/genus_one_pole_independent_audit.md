# Independent audit of the genus-one pole obstruction

Status: PASS, 9 November 2026. The failed candidate is
Y^2=1+b(1+bv^2)^2. This audit rules out completeness on all prepared
inputs. It does not rule out a restricted prime-pattern family.

## General odd-valuation extraction

Let p be odd, v_p(kappa)=0, and nu=v_p(R) odd. In
y^2=T^2+kappa R(1+R s^2)^2,
the valuation of1+R s^2 is min(0,nu+2v_p(s))<=0, since its
two possible finite valuations cannot tie. This includes s=0.
The second summand has odd valuation, whereas T^2 has even valuation
when T is nonzero. A rational square on the left therefore forces
T nonzero and
2v_p(T)<nu+2v_p(1+R s^2)<=nu.
There is no zero-y exception because the summands cannot cancel.

If T=Tr(W^(-1)) for nonzero W over an unramified quadratic completion
and ell=max_{w|p}v_w(W), the trace inequality gives v_p(T)>=-ell.
Hence ell> -nu/2, the desired local extraction inequality.
For T nonzero, the change b=R/T^2, v=Ts, Y=y/T transforms the
candidate into Y^2=1+kappa b(1+bv^2)^2 exactly.

## A negative-even-valuation obstruction

Suppose p is odd, -1 is a square in its residue field,
v_p(b)=-2m<0, and the unit part of b is a nonsquare. For any v,
the valuation of b v^2 is even. If it is zero, its residue is a
nonsquare and therefore cannot be-1. In every case
v_p(1+bv^2)=min(0,v_p(bv^2))<=0.
Consequently b(1+bv^2)^2 has negative even valuation and nonsquare
unit part. Adding1 preserves that leading unit, so it cannot be
a square. This excludes all affine solutions over Q_p.

## Exact prepared input

Take b=409(204/1013)^2=17020944/1026169. Then
17*1026169-17020944=423929>0, proving0<b<17.
The reduced denominator is1013^2. Its valuations at2,3,17 are4,2,2.
Since409 is1 modulo8,3,17, b is a square in each ofQ_2,Q_3,Q_17.
Thus it satisfies all stated preparation conditions, including the
lower bounds3,1,2 at the three primes.

Trial division through31 proves1013 prime. It is1 modulo4, and
the exact Euler calculation409^506 mod1013 is1012. At this prime
v(b)=-2 and the unit part has nonsquare class409. The preceding
obstruction applies.

The quartic b^3v^4+2b^2v^2+(b+1) is separable for b>0:
its derivative can vanish at a root only if b=0 or b=-1.
Its smooth projective completion has genus one. The points at
infinity would require the square root of b^3, also absent over
Q_1013. Hence even that completion has no Q_1013-point.

The exact integer computations were independently executed with
Python integer arithmetic and fractions; no floating-point decision
was used.

## Final finite-coefficient strengthening

The final paper
`papers/pole_parameters/quartic_pole_obstruction_20261109_v17.tex`
and its checker were subsequently read and independently checked:
PASS. The checker reports the exact first input and all preparation
and Euler data above.

Its Corollary3.3 is also valid for any finite nonempty set of fixed
nonzero rational kappa. In reduced forms kappa=a_k/d_k, put
M=408*product|a_k*d_k|. Since M>=408, the cyclotomic value
Phi_M(M)>1. A prime divisor p does not divide M, because
Phi_M(0)=1. The factorization of x^M-1 modulo p is separable;
therefore a root of Phi_M has exact order M. It follows that
p=1 modM. This elementary construction requires no assumption
about primes in arithmetic progressions.

Quadratic reciprocity, p=1 mod8, and p=1 modulo every odd prime
factor of the fixed numerators and denominators imply that each
kappa is a p-adic unit with square residue. This includes negative
kappa because-1 is a square modulo p. The Chinese remainder theorem
gives positive c=1 mod408 with nonsquare residue modulo p. For all
sufficiently large m, b_m=c(204/p^m)^2 satisfies every preparation
condition and tends to zero. Its leading unit at p is nonsquare,
so the local obstruction applies simultaneously to every kappa.

There is no singular-curve exception for negative kappa: the valuation
of kappa*b_m is-2m, hence1+kappa*b_m is nonzero, while the
quadratic-in-v^2 discriminant is-4*kappa*b_m^3, also nonzero.
The same infinity-point argument applies.
