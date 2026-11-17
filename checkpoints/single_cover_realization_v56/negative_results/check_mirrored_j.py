#!/usr/bin/env python3
import sympy as s
A,w,x=s.symbols('A w x')
j=(A*A+192)**3/(A*A-64)**2
assert s.cancel(j-1728-A*A*(A-24)**2*(A+24)**2/(A*A-64)**2)==0
assert s.cancel(j-287496-(A*A-72)*(A*A-528*A-4032)*(A*A+528*A-4032)/(A*A-64)**2)==0
assert s.expand((x*x+4-(w-4)*x)*(x*x+4+(w-4)*x)
                -(x**4+(-w*w+8*w-8)*x*x+16))==0
print('PASS: exact j factorizations and Jacobi quadratic factorization')
