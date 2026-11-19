from fractions import Fraction as F
import sympy as s
v=s.symbols("v"); p=(v+4)*(v+20)**3*(v-5)**2; q=(v-4)*(v-20)**3*(v+5)**2
assert s.expand(p-q)==108*v**5 and s.gcd(p,q)==1
theta={F(0)}|{F(1,r-21) for r in [0,4,-4,5,-5,20,-20]}
assert len(theta)==8 and min(theta)==-1 and max(theta)==0
for kap,e,k,expected in [(F(121,100),6,6,F(8374,14641)),(F(16,15),4,5,F(99,160))]:
    rate=(12/kap-8-F(8,k))*(e/kap-3)/2
    assert rate==expected and rate>F(1,2)
print("Degree-six identity, eight rational contacts, and both strict height inequalities verified.")
