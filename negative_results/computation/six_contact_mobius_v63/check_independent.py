#!/usr/bin/env python3
"""Independent exact controls for the every-integer extension."""
from pathlib import Path
from math import isqrt, prod
import json, hashlib, argparse
HERE=Path(__file__).resolve().parent
ROOT=HERE if (HERE/'certificate.json').exists() else HERE.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--certificate',type=Path,default=ROOT/'certificate.json')
parser.add_argument('--source',type=Path)
parser.add_argument('--output',type=Path,default=HERE/'independent_odd_extension_certificate.json')
args=parser.parse_args()
if args.source is None:
    filename='six_contact_mobius_obstruction_20261117_v63.tex'
    candidates=[ROOT/filename, ROOT.parents[2]/'negative_results/papers/pole_parameters'/filename]
    args.source=next((p for p in candidates if p.exists()),None)
    if args.source is None: parser.error('Use --source to specify the audited manuscript.')
certificate=json.loads(args.certificate.read_text())
recurrences=0
for row in certificate['group']['automorphisms'][2:]:
    aa,bb,cc,dd=row['matrix']
    c=-dd*aa+2*cc*bb
    kk=4*bb*cc*(aa*dd-bb*cc)
    def gap(e):return 2*dd*dd*57**e+(2*dd*dd-abs(kk))*16**e+2*c*4**e-1
    assert gap(4)>0
    assert dd*dd>=1 and c<=5
    for e in range(4,67):
        assert gap(e+1)-16*gap(e)==82*dd*dd*57**e-24*c*4**e+15>0
        recurrences+=1
rows=[]; crt_residue,crt_modulus=1,2
for fixture in certificate['simultaneous_finite_menu']['fixtures']:
    e,p,y,B=(fixture[k] for k in ('exponent','prime','binomial_root','shift_residue_mod_p_squared'))
    assert all(p%d for d in range(2,isqrt(p)+1))
    assert pow(2,(p-1)//2,p)==p-1
    m=57**e-4**(e+1)
    assert (pow(y,e,p)+m)%p==0 and e*pow(y,e-1,p)%p
    mod=p*p
    a=(pow(B+1,e,mod)+pow(57,e,mod)*pow(pow(4,e,mod),-1,mod))%mod
    assert (a-4)%p==0 and (a-4)%mod!=0
    lam=-(a+1)*pow(5*a,-1,mod)%mod
    vals=[]
    for t in (lam,a*lam%mod):
        assert (t-1)%p
        f=prod([t,t+1,2*t+1,3*t+1,4*t+1,5*t+2])*pow(120,-1,mod)%mod
        assert f%p==0 and f!=0
        vals.append(f)
    crt_residue+=crt_modulus*((B-crt_residue)*pow(crt_modulus,-1,mod)%mod)
    crt_modulus*=mod
    rows.append({'e':e,'p':p,'shift_residue':B,'contact_values_mod_p2':vals})
assert crt_residue==certificate['simultaneous_finite_menu']['common_odd_shift']
assert crt_modulus==certificate['simultaneous_finite_menu']['progression_modulus']
report={'status':'PASS','source_sha256':hashlib.sha256(args.source.read_bytes()).hexdigest(),
 'independent_one_step_recurrence_checks':recurrences,'prime_fixtures':rows,
 'odd_progression_residue':str(crt_residue),'modulus':str(crt_modulus),
 'scope':'Exact recurrence and nine fixture controls; odd root-field and all-exponent claims are proved in the audit, not inferred from sampling.'}
args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','recurrences':recurrences,'prime_fixtures':len(rows)},indent=2))
