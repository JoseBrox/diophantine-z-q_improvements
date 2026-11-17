# Two limitations on matching the new rational levels

These are scoped checkpoint statements; they give no variable lower bound.

## Square levels are equivalent to the zero-level covering

Fix a prepared input d and put eta=1-d. Define
k(r)=eta(d+r^2)/(d-r^2), h(r)=2d eta r/(d-r^2).
Then h(r)^2=d(k(r)^2-eta^2).

There is a rational r for which k(r) is a rational square if and only if the zero-level curve
C_0: y^2=d(eta^2-s^4)
has a rational point.

Proof in the forward direction: write k(r)=t^2. Its nonzero value and eta>0 imply t nonzero. Put
s=eta/t, y=eta h(r)/t^2.
The displayed norm identity gives y^2=d(eta^2-s^4).

Conversely, any point (s,y) of C_0 has s nonzero, since otherwise d would be a rational square. Put
t=eta/s, h=eta y/s^2, r=h/(t^2+eta).
Then h^2=d(t^4-eta^2) and
r^2=d(t^2-eta)/(t^2+eta).
Thus d-r^2=2d eta/(t^2+eta) is nonzero and k(r)=t^2. Zero ordinates are included.

The already certified prepared counterexample d=112/225 has no rational point on C_0. Therefore demanding a square k is not a universally complete specialization. The explicit good level k=3364/675 for this d is nonsquare.

If eta is a rational square, every rational r does have the immediate point s^2=eta, y=h(r). This recovers the square-complement condition, whose realization on actual detector inputs is still open. This immediate point alone makes no assertion of infinitely many points or every guard on every individual fiber.

Source of the counterexample: negative_results/papers/pole_parameters/prepared_sha_obstruction_20261117_v57.tex in the published repository. The equivalence above is elementary and was checked independently by the root.

## Local analytic lifting does not establish rational lifting

An etale map near a rational point can admit analytic lifts after arbitrarily accurate local approximation while the perturbed value has no rational lift.

For Y^2=T at (T,Y)=(1,1), let S be any finite prime set and choose a nonzero positive N divisible by sufficiently high powers of all primes in S. Choose a large prime q outside S with q not dividing N, and set T=1+N/q. This is arbitrarily close to 1 in R and in every prescribed S-adic neighborhood, and is a square in each selected completion when N has sufficient local divisibility. But v_q(T)=-1, so T is not a rational square.

The varying-level approximation theorem therefore does not justify exact global squares after perturbing actual detector coordinates. A valid elimination would need a rational section, a rationally invertible existing coordinate, or a global rational-point theorem for the constrained incidence. No such elimination is established here.
