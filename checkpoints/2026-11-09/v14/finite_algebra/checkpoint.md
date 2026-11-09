# Finite-algebra elimination research

The intended new construction keeps the 27 or 29 external variables and the
same arithmetic premises. It replaces the large selector product by an
explicitly separating element on the part where the source guard is nonzero.
The construction below is undergoing independent audit and is not yet a
published degree claim.

Exact source inspection shows that the first nine monic quartics have scalar
coefficients and are separable at every rational base. Their tensor product B
is therefore etale of rank b=4^9. Each later relation is q_j^2=c_j with c_j in
B, and the source guard has the form g*product(q_j), with g in B. Thus T=G^2
belongs to B; the part where T is nonzero is etale even in the larger algebra
A. This inspection was performed on both pinned source DAGs.

Write det_B(1-vT)=sum a_j v^j. For r=1,...,b set c=a_r,
h_r(z)=sum_{j=0}^r a_j z^(r-j), E=c-h_r(T). On the degree-r case (a_j=0 for
j>r and c nonzero), E/c is the idempotent of the T-nonzero part. Let delta_i
be the native discriminants (nine scalar quartic discriminants followed by
the elements 4c_j). Define D_i=Norm_B(E*delta_i+c-E), D=product D_i^2.
Every D_i is nonzero on the correct case.

Let M_i be the native generator matrices of A, R=n(1+sum of all their entry
squares), S=b*sum_i d_i(d_i-1), K=(2R)^S*(1+c^2)^(mb)*product_i(1+D_i^2),
and C=D+4RK. Root-discriminant estimates give that distinct active characters
first differing in generator i differ there by at least D/K. Consequently
alpha=(C/D)^m+sum_i (C/D)^(m-i)*theta_i is nonzero and separates the active
characters. Here i=1,...,m.

The entirely polynomial multiplication element
beta=c*D*E*(C^m+sum_i D^i*C^(m-i)*theta_i)
equals a nonzero rational scalar times alpha on the active part and zero on
the inactive part. Its determinant H_r(U)=det_A(1-U beta) has a rational
root exactly when the correct case has a rational character with G nonzero.
If c=0 or D=0, beta=0 and H_r=1. The polynomial
product_{r=1}^b (H_r(U)^2+sum_{j>r}a_j^2)
therefore has exactly the guarded source projection. No new external
variable or genericity assumption is introduced.

Next tasks: full degree and coefficient bounds, an exact indexed recipe,
small-dimensional degeneration tests, and independent proof review. Earlier
provisional-bounds27/29 files concern the stronger all-branches-regular
special case and remain explicitly provisional; they must not be confused
with this universally applicable construction.
