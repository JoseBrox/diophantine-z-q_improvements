#!/usr/bin/env python3
"""Compose the retained coordinate maps exactly, including both contact weights."""
import argparse,hashlib,json
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent
REL='computation/quartic/affine_laurent195_v45/quadratic-family.json'
def locate_repo(supplied):
    if supplied:return supplied
    for p in [HERE]+list(HERE.parents):
        for root in (p,p/'repo'):
            if (root/REL).is_file():return root
    raise FileNotFoundError('Supply --repo pointing to the source repository.')

def run(root,output):
    inputs={}
    def read(relative):
        raw=(root/relative).read_bytes();inputs[relative]=hashlib.sha256(raw).hexdigest();return json.loads(raw)
    parent=read('sources/h10_quartic198/circuits/inverse198/quadratic.json')
    la38=read('computation/quartic/laurent_recovery_v38/family196/certificate.json')
    bal=read('computation/quartic/laurent_recovery_v38/family196/balancing.json')
    old196=read('computation/quartic/laurent_recovery_v38/family196/balanced-quadratic.json')
    paired=read('computation/quartic/paired_redundancy196_v40/balanced-quadratic.json')
    primitive=read('computation/quartic/primitive_basis196_v40/transform.json')
    tr=read('computation/quartic/affine_laurent195_v45/transformation.json')
    final=read(REL)
    assert old196['coordinates']==paired['coordinates']
    parent_names={c['id']:c['name'] for c in parent['coordinates']}
    chosen=[15,16,19,20,33,34,35,36,64,65,66,67,68,69,77,78,92,93,94,153,154]
    records=[]
    for old in chosen:
        i=int(la38['old_to_new'][str(old)])
        assert la38['weights'].get(str(old),[0,0,0])==[0,0,0]
        assert Fraction(la38['constants'].get(str(old),'1'))==1
        assert Fraction(primitive['coordinate_scaling'].get(str(i),'1'))==1
        assert str(i) not in tr['affine_substitutions']
        new=int(tr['laurent']['old_to_new'][str(i)])
        # Retained power coordinates77,78 preserve their values; other selected
        # coordinates have source=C^b*w0^ell*target before the final C scaling.
        ell=tr['laurent']['weights'].get(str(i),[0])[0]
        assert str(i) not in tr['laurent']['constants'] or Fraction(tr['laurent']['constants'][str(i)])==1
        b=bal['weights'].get(str(i),0)
        p=tr['parameter_scaling']['weights'].get(str(new),0)
        records.append({'physical_parent_coordinate':old,'parent_name':parent_names[old],
            'coordinate196':i,'coordinate195':new,'balanced_C_exponent':b,
            'Laurent_w0_exponent':ell,'final_C_exponent':p,
            'physical_equals_C_power_q0_power_final_coordinate':[b+p,-ell,new]})
    by={r['physical_parent_coordinate']:r['physical_equals_C_power_q0_power_final_coordinate'] for r in records}
    expected={15:[0,-1,15],16:[0,-1,16],19:[0,-1,19],20:[0,-1,20],
      33:[1,-1,33],34:[1,-1,34],35:[1,-1,35],36:[1,-1,36],
      64:[0,-1,64],65:[0,-1,65],66:[1,-3,66],67:[1,-3,67],
      68:[1,-3,68],69:[1,-3,69],77:[0,0,77],78:[0,0,78],
      92:[0,1,90],93:[0,-1,91],94:[0,-1,92],153:[0,-1,150],154:[0,-1,151]}
    assert by==expected
    # Check the decisive final square identities literally, including the
    # product-style half-imaginary coordinate and the fixed parameter C.
    rows={r['name']:r for r in final['residuals']}
    def parsed(row):return {(int(t['parameterPower']),tuple(t['monomial'])):Fraction(t['coefficient']) for t in row['terms']}
    def addterm(poly,a,m,c):
        key=(a,tuple(sorted(m)));poly[key]=poly.get(key,Fraction(0))+c
        if not poly[key]:del poly[key]
    def square(poly,a,terms,multiplier):
        for x,c in terms:
            for y,d in terms:addterm(poly,a,(x,y),multiplier*c*d)
    real={(0,(66,78)):Fraction(1)}
    square(real,1,[(33,1),(35,-1)],-1);square(real,1,[(34,1),(36,1)],-2)
    imag={(0,(67,78)):Fraction(1)}
    for x,c in [(33,1),(35,-1)]:
        for y,d in [(34,1),(36,1)]:addterm(imag,1,(x,y),-c*d)
    assert parsed(rows['testSquare.40.1.0.definition'])==real
    assert parsed(rows['testSquare.40.1.1.definition'])==imag
    hs0={(0,(15,16)):Fraction(1),(0,(65,77)):Fraction(-1)}
    hs1={(0,(15,15)):Fraction(1),(0,(16,16)):Fraction(2),(0,(64,77)):Fraction(-1)}
    assert parsed(rows['testSquare.40.0.0.definition'])==hs0
    assert parsed(rows['testSquare.40.0.1.definition'])==hs1
    factor_outputs=[]
    c_profile=[1,1,1,0,-1]
    for detector in (0,1):
        for factor in range(5):
            for component in (0,1):
                old=121+16*detector+2*factor+component
                i=int(la38['old_to_new'][str(old)])
                first_weight=la38['weights'].get(str(old),[0,0,0])
                assert first_weight==([0,-2,0] if detector==0 else [1,0,-2])
                assert Fraction(la38['constants'].get(str(old),'1'))==1
                assert Fraction(primitive['coordinate_scaling'].get(str(i),'1'))==1
                assert str(i) not in tr['affine_substitutions']
                new=int(tr['laurent']['old_to_new'][str(i)])
                b=bal['weights'].get(str(i),0)
                ell=tr['laurent']['weights'].get(str(i),[0])[0]
                p=tr['parameter_scaling']['weights'].get(str(new),0)
                # PhysicalPhi=R^(-detector)*original198slot. The R powers
                # cancel in the first Laurent map, leaving physical_q_j^2.
                unit=[2-ell,2*detector]
                assert unit==[1,2*detector] and b+p==c_profile[factor]
                assert new==118+16*detector+2*factor+component
                factor_outputs.append({'detector':detector,'factor':factor,'component':component,
                    'source198_coordinate':old,'source196_coordinate':i,'source195_coordinate':new,
                    'C_exponent':b+p,'unit_exponent_in_u_v':unit})
    report={'status':'PASS','arithmetic':'exact integers and rationals; standard library only',
      'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'input_sha256':inputs,'diagonal_maps':records,
      'fixed_parameter':'C=149^N',
      'physical_field_identities':{
       'f(H)':'q0^(-1)*(x15+x16*rho)',
       'L2':'C*q0^(-1)*(x33+x34*rho)',
       'L2^0':'C*q0^(-1)*(x35+x36*rho)',
       'C2^2':'C*q0^(-3)*(x66+2*x67*rho)',
       'C3^2':'C*q0^(-3)*(x68+2*x69*rho)',
       'D_H^2':'q0^(-1)*(x64+2*x65*rho)',
       'B0^2':'q0^(-1)*(x19+2*x20*rho)',
       'T_H':'q0^(-1)*(x150+x151*rho)'},
      'physical_contact_weights':{'first':'q0=x77','second':'q1_physical=q0*x90'},
      'physical_factor_output_maps':factor_outputs,
      'physical_factor_output_formula':'Phi_jk=C^[1,1,1,0,-1]_k*u*v^(2*j)*(x_[118+16*j+2*k]+rho*x_[119+16*j+2*k])',
      'formal_unit_coordinates':{'x77':[1,0],'x78':[-1,0],'x90':[0,1],'x91':[0,-1],'x92':[-1,-2]},
      'formal_unit_basis':'u=x77=q0; v=x90=q1_physical/q0',
      'physical_weight_directions':{'first':[1,0],'second':[1,1]},
      'corrected_second_factor_unit_exponents':{'q1_physical^11*C2^4':[5,11],'q1_physical*A1^2':[1,1]},
      'verification_note':'All selected maps are diagonal. The paired stage only deletes rows; no selected coordinate is changed by the primitive coordinate scaling or affine centering.'}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in('input_sha256','diagonal_maps','physical_factor_output_maps')},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',type=Path)
    ap.add_argument('--output',type=Path,default=HERE/'mapping_certificate.json')
    args=ap.parse_args();run(locate_repo(args.repo),args.output)
