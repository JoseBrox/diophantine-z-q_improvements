"""Remove ten point, positivity and odd-valuation guards in certified order."""
from pathlib import Path
import sys,json,math,argparse
from functools import cache
HERE=Path(__file__).resolve().parent
REPO=HERE.parent.parent/'diophantine'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo',type=Path,default=REPO)
parser.add_argument('directories',nargs='*',type=Path)
settings=parser.parse_args()
REPO=settings.repo.resolve()
sys.path.insert(0,str(REPO/'computation/few_variables/trace27_nontorsion'))
from field_circuit import Circuit,Rational

def improve(directory):
 source=json.loads((directory/'native.json').read_text());parent=json.loads((directory/'polynomial.json').read_text());cert=json.loads((directory/'compact.json').read_text())
 c=Circuit()
 for i,row in enumerate(source['coefficient_dag']):assert c.node(*row)==i
 @cache
 def ff(i):
  op,*a=c.nodes[i]
  if op=='int':return set()
  if op in ['neg','pow']:return ff(a[0]) if op=='neg' or a[1] else set()
  if op=='mul':return set().union(*(ff(j) for j in a))
  return {i}
 rat=lambda r:Rational(c,r['numerator'],r['denominator'])
 m=next(e for e in source['events'] if e['operation']=='moving_contacts')
 pole=next(e for e in source['events'] if e['operation']=='rescaled_zero_pole')
 p,q,u=map(rat,[m['p'],m['q'],m['u']]);f=p*p+q**3
 a_positive=ff(u.d)|ff(f.n)
 a_normalizer=ff((1+u).n)
 a_pole=ff(pole['e']['denominator'])-a_positive
 points=[e for e in source['events'] if e['operation']=='point_block']
 def point_norm(point):
  h0,h1=map(rat,point['h'])
  return ff((h0*h0-2*h1*h1).n)
 a_root_ordinate=ff(source['finite_blocks'][0]['variable_nodes'][-1])
 a_auxiliary=set().union(*(point_norm(p) for p in points[1:]))
 a_root_abscissa=point_norm(points[0])
 stages={'pre_character_root_ordinate':sorted(a_root_ordinate),'pre_character_auxiliary_abscissas':sorted(a_auxiliary),'post_character_root_abscissa':sorted(a_root_abscissa),'positive_contact_sums':sorted(a_positive),'odd_weight_normalizer':sorted(a_normalizer),'odd_squareclass_conic':sorted(a_pole)}
 auto=set().union(*(set(s) for s in stages.values()))
 kept=set(cert['retained_norm_atoms']);assert auto<=kept
 kept-=auto
 factors={r['node']:r for r in parent['subalgebra_norm_factors']}
 degree=sum(factors[i]['scalar_norm_degree_bound'] for i in kept)
 gain=sum(factors[i]['scalar_norm_log2_l1_bound'] for i in auto)
 cert['additional_automatic_guards']=stages
 cert['recovery_order']=['pre_character_root_ordinate','pre_character_auxiliary_abscissas','point_separator_and_rational_character','post_character_root_abscissa','retained_point_and_contact_units','positive_contact_sums','odd_weight_normalizer','positive_balancing_atoms','positive_product_atoms','odd_squareclass_conic']
 cert['retained_norm_atoms']=sorted(kept)
 cert['guard_degree']=degree
 cert['degree_bound']=cert['rank']*(1+degree+cert['separator_degree'])+1
 cert['coefficient_log2_l1']-=cert['rank']*gain
 cert['coefficient_double_power']=cert['coefficient_log2_l1'].bit_length()
 d=cert['degree_bound']-1;v=cert['variables'];n=cert['rank']
 cert['support_power']=(math.comb(d+v,v)-math.comb(d-n+v-1,v)).bit_length()
 cert['proof']='weak11_audit_and_transfer.tex; root ordinate and auxiliary abscissas before character extraction, root abscissa afterward, then contact positivity, odd valuation, detector factors and conic denominator'
 (directory/'strengthened.json').write_text(json.dumps(cert,sort_keys=True,separators=(',',':'))+'\n')
 print(directory.name,{k:cert[k] for k in ['guard_degree','degree_bound','support_power','coefficient_log2_l1']},stages)
if __name__=='__main__':
 paths=settings.directories or [HERE/'full_eight',HERE/'full_eight_strong']
 for path in paths:improve(path)
