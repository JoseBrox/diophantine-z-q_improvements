#!/usr/bin/env python3
"""Exact checks of the v30 common-twist applications, not of the source theorem."""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'sources/hexagon/jaswal_row5a_audit_and_simultaneous_twists_20261113.tex'

def require(ok,message):
    if not ok:raise AssertionError(message)

def zero(f,message):require(s.cancel(f)==0,message)

def prepared(b):
    require(0<b<1 and isqrt(b.denominator)**2==b.denominator,'Real range and square denominator')
    a,d=b.numerator,b.denominator
    v=(a&-a).bit_length()-(d&-d).bit_length()
    require(v>=4 and v%2==0,'2-adic valuation')
    unit=b/Q(2)**v
    require(unit.numerator*pow(unit.denominator,-1,8)%8==1,'2-adic square unit')

def admissible(beta,theta):
    require(beta>1 and beta%8==theta%8==1,'Admissible residues')
    require(gcd(beta,theta)==1,'Coprimality with input class')
    for n in (beta,theta):require(all(e==1 for e in s.factorint(n).values()),'Squarefree representative')
    for p in s.factorint(beta):require(pow(theta%p,(p-1)//2,p)==1,'Complement residue symbol')
    for p in s.factorint(theta):require(pow(beta%p,(p-1)//2,p)==1,'Input residue symbol')

def run():
    beta,z,c,e,w,p,q=s.symbols('beta z c e w p q',nonzero=True)
    theta=s.symbols('theta',positive=True)
    # Reduce the source equations by the two explicitly stated square equations.
    pp=(1-e*e)/beta;qq=(w**4-e*e*theta**2)/(beta*w*w)
    b=beta*z*z;pi=p/z;ui=c*w;vi=e*theta*c/w;qi=c*q/z
    zero((e*e+b*pi*pi-1).subs(p*p,pp),'First pole equation')
    zero(ui*vi-e*theta*c*c,'Middle pole equation using 1-b=theta*c^2')
    zero((ui*ui-vi*vi-b*qi*qi).subs(q*q,qq),'Last pole equation')
    zero((w**4-e*e*theta**2-beta*w*w*p*p).subs({theta:1,w:1}).subs(p*p,pp),'Trivial complement')
    x,y,m,eta,h=s.symbols('x y m eta h')
    zero((h**3*y)**2-(h**2*x)**3+(m*eta*h**2)**2*(h**2*x)-h**6*(y*y-x**3+(m*eta)**2*x),'Change-of-base isomorphism')
    require(s.cancel(ui*ui-vi*vi-b*(c*q)**2).subs(q*q,qq)!=0,'Missing z denominator corruption detected')
    examples=[]
    for inputs,complements,delta in [
            ((Q(272,361),Q(1088,1225)),(89,137),1),
            ((Q(2448,14641),Q(4352,27225)),(89*137,89*257),89)]:
        for b0,th in zip(inputs,complements):
            prepared(b0);admissible(17,th)
            for val in (b0/17,(1-b0)/th):
                require(isqrt(val.numerator)**2==val.numerator and isqrt(val.denominator)**2==val.denominator,'Exact square classes')
        transformed=[]
        for th in (1,*complements):
            common=gcd(delta,th);et=delta*th//(common*common)
            require(delta*th==et*common*common,'Squarefree class translation')
            admissible(17,et)
            if et!=1 and et not in transformed:transformed.append(et)
        require(all(gcd(x,y)==1 for i,x in enumerate(transformed) for y in transformed[i+1:]),'Translated complements disjoint')
        examples.append(dict(inputs=[str(x) for x in inputs],input_squareclass=17,
            complement_squareclasses=list(complements),base_change=delta,
            translated_classes=transformed,retained_parameters=3,
            explicit_twist_computed=False))
    require(gcd(89*137,89*257)!=1,'Original overlapping pair is not disjoint')
    return dict(schema='common-twist-exact-checks/v30',status='PASS',symbolic_identities=5,
        prepared_examples=examples,negative_controls=2,source_audit_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        global_variable_count_improvement=False,source_twist_theorem_reproved_by_checker=False,
        scope='Exact witness identities, prepared-input conditions, square classes, primality/factorization and residue symbols. The finite-family source theorem is an explicit arithmetic input; no full defining polynomial with fewer variables is certified.')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path);args=ap.parse_args();report=run()
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
