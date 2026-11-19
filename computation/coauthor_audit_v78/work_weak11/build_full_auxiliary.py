"""Audited coauthor weak11 weight in the project's full auxiliary point charts."""
from pathlib import Path
from fractions import Fraction
import importlib.util,sys,json,argparse
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/'H10-eleven-variables'
REPO=HERE.parent.parent/'diophantine'
ap=argparse.ArgumentParser()
ap.add_argument('--repo',type=Path,default=REPO)
ap.add_argument('--coauthor-root',type=Path,default=ROOT)
ap.add_argument('--strong',action='store_true');ap.add_argument('--e',type=int);ap.add_argument('--k',type=int);ap.add_argument('--output',type=Path);ap.add_argument('--shift',type=int,default=3)
ap.add_argument('--squareclass',choices=['original','reciprocal','polynomial','inverse_polynomial','flip_first','flip_second','flip_cubic'],default='original')
settings=ap.parse_args()
REPO=settings.repo.resolve();ROOT=settings.coauthor_root.resolve()
strong=settings.strong
output=settings.output or HERE/('full_eight_strong' if strong else 'full_eight')
sys.path.insert(0,str(ROOT/'counts/poles'))
sys.argv=[str(HERE/'build_full_auxiliary.py'),'--repo',str(REPO),'--eight']+(['--strong'] if strong else [])
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
co=load('co_weak11',ROOT/'counts/poles/build_weak11.py')
full=load('full_aux11',REPO/'computation/few_variables/full_auxiliary11_v71/build_source.py')
class FullWeak11(co.Weak11):
 def split_square(self,value):
  d,t=super().split_square(value)
  if settings.squareclass.startswith('flip_'):
   m=next(e for e in self.events if e['operation']=='moving_contacts')
   rat=lambda r:type(d)(self.c,r['numerator'],r['denominator'])
   p,q=rat(m['p']),rat(m['q']);k=m['band']
   factor={'flip_first':p+q**k,'flip_second':p**k+q,'flip_cubic':p**3+q**5}[settings.squareclass]
   return d/factor**2,t*factor
  if settings.squareclass=='reciprocal':return 1/d,d*t
  if settings.squareclass=='polynomial':
   den=type(d)(self.c,d.d,self.c.one)
   return d*den**2,t/den
  if settings.squareclass=='inverse_polynomial':
   num=type(d)(self.c,d.n,self.c.one)
   return d/num**2,t*num
  return d,t
 def point(self,name):
  if name=='A':return super().point(name)
  self.c.point_count+=1
  h=self.abscissas[name];a,b=self.sub(self.mul(self.square(h),h),self.mul(self.D,h))
  u=self.c.variable(name+'.U','finite.point_block');v=self.c.variable(name+'.V','finite.point_block');w=self.c.variable(name+'.W','finite.point_block')
  j=self.remember_norm((u/2,v/2),w)
  point={'h':h,'j':j,'x':h,'y':j}
  self.relations.append(dict(name=name,kind='point_block',degree=4,A=self.rr(a),B=self.rr(b),variable_nodes=[u.n,v.n,w.n]))
  self.inv(h);self.inv(j)
  self.events.append(dict(operation='point_block',name=name,chart='full_auxiliary',h=[self.rr(q) for q in h],A=self.rr(a),B=self.rr(b),j=[self.rr(q) for q in j],x=[self.rr(q) for q in h],y=[self.rr(q) for q in j]))
  return point
builder=FullWeak11(settings.shift)
if settings.e is not None:builder.scale_power=settings.e
if settings.k is not None:builder.band=settings.k
source=builder.build()
source['name']+='_full_auxiliary'
source['squareclass_normalization']=settings.squareclass
source['auxiliary_chart']='H,U: x=h, y=j, j^2=h^3-Dh; A retains x=h^2'
changes=full.patch_compiler()
parent=full.old._subalgebra.compile_specification(source)
from finite_bounds import encode
cert=encode(source,parent)
output.mkdir(exist_ok=True)
for name,obj in [('native',source),('polynomial',parent),('compact',cert),('compiler_adjustments',changes)]:
 (output/(name+'.json')).write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n')
print(json.dumps({k:cert[k] for k in ['variables','degree_bound','rank','guard_degree','separator_degree','support_power','coefficient_double_power']},indent=2))
