from fractions import Fraction as Q
from math import gcd
import json
from pathlib import Path
th=[Q(0),Q(-1,2),Q(-1),Q(1,2399),Q(-32,407)]
def R(t):
    ans=Q(1)
    for u in th: ans*=((t-1)**2-(1-u)**2)/(t-1)**2
    return ans
for T in map(Q,[10,100,10000]):
    l=1-T/2
    assert R(l)==R(l+T)
    assert 0<R(l)<1
    assert R(l)*R(l+T)==R(l)**2
X=Q(1,357); beta=51*X*X+2504;b=1251499;t=2504*b+1
assert gcd(t,b)==1
assert t*t-beta*t*b+b*b==1
assert X.denominator>1
report={'reflection_fixture_checks':3,'direct_beta_counterexample':{'X':str(X),'beta':str(beta),'t':t,'b':b,'gcd':gcd(t,b),'norm':str(t*t-beta*t*b+b*b)},'scope':'Exact finite counterexample and reflection fixtures. Universal reflection identity and monicity statements proved in accompanying note; no new quartic record claimed.'}
Path(__file__).with_name('verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
