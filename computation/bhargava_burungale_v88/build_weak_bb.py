"""Build the weak-abc eleven-variable circuits with the BB v2 product pole.

Only the final pole is changed.  The input is 7*b, with the original b,
contact scalar, point charts, all six tests, and detector product retained.
"""
from pathlib import Path
from functools import cache
from fractions import Fraction
import argparse, importlib.util, json, math, sys

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--work-root',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--strong',action='store_true')
parser.add_argument('--shift',type=int,default=3)
parser.add_argument('--e',type=int)
parser.add_argument('--k',type=int)
parser.add_argument('--normalization',choices=['original','reciprocal','polynomial','inverse_polynomial','flip_first','flip_second','flip_cubic','weight'],default='original')
settings=parser.parse_args()
WORK=settings.work_root.resolve();REPO=WORK/'diophantine'
ARCHIVE=WORK/'audit_20261119/H10-eleven-variables'
POLES=ARCHIVE/'counts/poles'
sys.path.insert(0,str(POLES))
sys.argv=['build_weak_bb.py','--repo',str(REPO),'--eight']+(['--strong'] if settings.strong else [])

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path)
 mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod)
 return mod

co=load('bb_weak_upstream',POLES/'build_weak11.py')
full=load('bb_weak_full_chart',REPO/'computation/few_variables/full_auxiliary11_v71/build_source.py')
from field_circuit import Rational

class BBWeak11(co.Weak11):
 def point(self,name):
  if name=='A':return super().point(name)
  self.c.point_count+=1
  h=self.abscissas[name]
  a,b=self.sub(self.mul(self.square(h),h),self.mul(self.D,h))
  u=self.c.variable(name+'.U','finite.point_block')
  v=self.c.variable(name+'.V','finite.point_block')
  w=self.c.variable(name+'.W','finite.point_block')
  j=self.remember_norm((u/2,v/2),w)
  point={'h':h,'j':j,'x':h,'y':j}
  self.relations.append(dict(name=name,kind='point_block',degree=4,A=self.rr(a),B=self.rr(b),variable_nodes=[u.n,v.n,w.n]))
  self.inv(h);self.inv(j)
  self.events.append(dict(operation='point_block',name=name,chart='full_auxiliary',h=[self.rr(q) for q in h],A=self.rr(a),B=self.rr(b),j=[self.rr(q) for q in j],x=[self.rr(q) for q in h],y=[self.rr(q) for q in j]))
  return point
 def split_square(self,value):
  d,t=super().split_square(value)
  rat=lambda r:Rational(self.c,r['numerator'],r['denominator'])
  m=next(e for e in self.events if e['operation']=='moving_contacts')
  p,q=rat(m['p']),rat(m['q']);k=m['band']
  mode=settings.normalization
  if mode.startswith('flip_'):
   factor={'flip_first':p+q**k,'flip_second':p**k+q,'flip_cubic':p**3+q**5}[mode]
   return d/factor**2,t*factor
  if mode=='reciprocal':return 1/d,d*t
  if mode=='polynomial':
   den=Rational(self.c,d.d,self.c.one);return d*den**2,t/den
  if mode=='inverse_polynomial':
   num=Rational(self.c,d.n,self.c.one);return d/num**2,t*num
  if mode=='weight':
   detector=next(e for e in self.events if e['operation']=='detector')
   u=rat(m['u'])
   return 7*u,rat(detector['norm'])/((1+u)*rat(detector['W'][0]))
  return d,t
 def zero_pole(self,b,structural,label):
  self.c.pole_count+=1
  v,s=structural
  e=7*b
  self.c.nonzero(e,label+'.nonzero input')
  d,t=self.split_square(e)
  self.c.nonzero(d,label+'.square class')
  self.c.nonzero(t,label+'.square multiplier')
  radicand=(1-e)*(v**4-d**2)*(s**4-d**2)
  self.finite_square(label+'.q',radicand,kind='pole')
  self.relations[-1]['zero_stratum_rule']='The native graph retains its root guard for compilation; the final positive encoder suppresses this terminal root guard and permits zero radicand and zero root.'
  self.events.append(dict(operation='bb_product_pole',label=label,input=self.rr(e),unscaled_input=self.rr(b),square_class=self.rr(d),square_multiplier=self.rr(t),first_parameter=self.rr(v),second_parameter=self.rr(s),radicand=self.rr(radicand)))

builder=BBWeak11(settings.shift)
if settings.e is not None:builder.scale_power=settings.e
if settings.k is not None:builder.band=settings.k
kappa=Fraction(16,15) if settings.strong else Fraction(121,100)
alpha=Fraction(builder.scale_power)/kappa-3
gamma=12/kappa-8-Fraction(8,builder.band)
assert builder.scale_power>0 and builder.band>=2 and alpha>0 and gamma>0 and alpha*gamma>1, 'Parameters do not satisfy the strict weak-abc height inequality'
source=builder.build()
source['name']+='_bb_v2_'+settings.normalization
source['squareclass_normalization']=settings.normalization
source['auxiliary_chart']='H,U: x=h, y=j, j^2=h^3-Dh; A retains x=h^2'
source['proof']='bb_product_degree_transfer_20261123_v88.tex, weak-abc section'
source['arithmetic_status']='Fixed weak rational abc at '+('16/15' if settings.strong else '121/100')+', retained elliptic, trace and prime-pattern premises, with prepared class-seven completeness supplied by Bhargava-Burungale v2 Lemma 2.2 and Theorem 2.3.'
source['final_pole_policy']={'terminal_zero_roots_allowed':True,'source_ordinate_guards_removed_by_final_encoder':True,'standalone_legacy_guarded_source_is_not_the_published_polynomial':True}
changes=full.patch_compiler()
parent=full.old._subalgebra.compile_specification(source)
from finite_bounds import encode
compact=encode(source,parent)

# Retain the old staged positivity and point recovery; the conic is absent.
nodes=source['coefficient_dag']
c=co.Circuit()
for i,row in enumerate(nodes):assert c.node(*row)==i
rat=lambda r:Rational(c,r['numerator'],r['denominator'])
@cache
def ff(i):
 op,*a=nodes[i]
 if op=='int':
  assert a[0]
  return set()
 if op in ('neg','pow'):return ff(a[0]) if op=='neg' or a[1] else set()
 if op=='mul':return set().union(*(ff(j) for j in a))
 return {i}
m=next(e for e in source['events'] if e['operation']=='moving_contacts')
p,q,u=map(rat,[m['p'],m['q'],m['u']])
positive=ff(u.d)|ff((p*p+q**3).n)
normalizer=ff((1+u).n)
points=[e for e in source['events'] if e['operation']=='point_block']
def point_norm(point):
 h0,h1=map(rat,point['h']);return ff((h0*h0-2*h1*h1).n)
stages={'pre_character_root_ordinate':sorted(ff(source['finite_blocks'][0]['variable_nodes'][-1])),
 'pre_character_auxiliary_abscissas':sorted(set().union(*(point_norm(p) for p in points[1:]))),
 'post_character_root_abscissa':sorted(point_norm(points[0])),
 'positive_contact_sums':sorted(positive),'odd_weight_normalizer':sorted(normalizer)}
auto=set().union(*(set(s) for s in stages.values()))
assert len(auto)==9
kept=set(compact['retained_norm_atoms']);assert auto<=kept
kept-=auto
rows={r['node']:r for r in parent['subalgebra_norm_factors']}
gd=sum(rows[i]['scalar_norm_degree_bound'] for i in kept)
gain=sum(rows[i]['scalar_norm_log2_l1_bound'] for i in auto)
final=dict(compact)
final['additional_automatic_guards']=stages
final['recovery_order']=['pre_character_root_ordinate','pre_character_auxiliary_abscissas','point_separator_and_rational_character','post_character_root_abscissa','retained_point_and_contact_units','positive_contact_sums','odd_weight_normalizer','positive_balancing_atoms','positive_product_atoms']
final['retained_norm_atoms']=sorted(kept)
final['guard_degree']=gd
final['degree_bound']=final['rank']*(1+gd+final['separator_degree'])+1
final['coefficient_log2_l1']-=final['rank']*gain
final['coefficient_double_power']=final['coefficient_log2_l1'].bit_length()
deg=final['degree_bound']-1;v=final['variables'];n=final['rank']
final['support_power']=(math.comb(deg+v,v)-math.comb(deg-n+v-1,v)).bit_length()
final['proof']='Nine staged point, contact, and normalizer deletions; terminal pole root allowed to vanish; class-seven preparation verified separately.'
settings.output.mkdir(parents=True,exist_ok=True)
for name,obj in [('native',source),('polynomial',parent),('compact',compact),('strengthened',final),('compiler_adjustments',changes)]:
 (settings.output/(name+'.json')).write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n')
print(json.dumps({'route':'strong' if settings.strong else 'weak','normalization':settings.normalization,**{k:final[k] for k in ['variables','degree_bound','rank','guard_degree','separator_degree','support_power','coefficient_double_power']}},sort_keys=True))
