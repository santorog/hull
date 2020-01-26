#!/usr/bin/python3

import numpy as np
import scipy.optimize as sco

# Bond 4-y, 3% per y
nom=100
zc=[0.025,0.029,0.032,0.034]
cf=[3,3,3,nom+3]

def price(cf_c,zc_r):
    value=0
    for i in range(0,len(cf_c)):
        value += cf_c[i] * np.exp(-(i+1)*zc_r[i])
    return value

print(price(cf, zc))

def price_act(r):
    new_zc=np.full(len(cf),r)
    return price(cf,new_zc)

def F(r):
    return price_act(r)-price(cf, zc)

print(sco.broyden1(F, 0.03))

def price_peer(c):
    size=len(cf)
    new_cf=np.full(size,c) 
    new_cf[size-1]+=nom
    return price(new_cf,zc)

def G(c):
    return price_peer(c)-nom

print(sco.broyden1(G, 0.03))
