#!/usr/bin/python3

import numpy as np
import scipy.optimize as sco
import utilities as ul

### Evaluation des obligations, taux actuariel, taux au pair

# Bond 4-y, 3% per y
nom=100
zc=[0.025,0.029,0.032,0.034]
cf=[3,3,3,nom+3]
mat=[1,2,3,4]

def price(cf_c,zc_r, mat_r):
    value=0
    for i in range(0,len(cf_c)):
        value += cf_c[i] * np.exp(-mat[i]*zc_r[i])
    return value

print("Le prix est : ",price(cf, zc, mat))

def price_act(r):
    new_zc=np.full(len(cf),r)
    return price(cf,new_zc, mat)

def F(r):
    return price_act(r)-price(cf, zc, mat)

print("Le taux actuariel est : ",ul.formatRate(sco.broyden1(F, 0.03), 100))

def price_peer(c):
    size=len(cf)
    new_cf=np.full(size,c) 
    new_cf[size-1]+=nom
    return price(new_cf,zc, mat)

def G(c):
    return price_peer(c)-nom

print("Le taux au pair est : ",ul.formatRate(sco.broyden1(G, 0.03), 1))

### Bootstrapping of 5 bonds

b_nom=np.full(5,100)             # nominal
b_mat=[0.25, 0.5, 1.0, 1.5, 2.0] # maturity
b_cp_y=[0,0,0,8,12]              # coupon yearly, paid semi-annually
b_pv=[97.5,94.9,90.0,96.0,101.6] # price
b_f=0.5                          # payment frequency

def cf_and_mat_for_year(f, yearly_coupon, mat, nom):
    nb= max(1,int(mat/f))

    # cf array
    cf_vect= np.full(nb, yearly_coupon * f)
    cf_vect[-1]+= nom 

    # mat array
    mat_vect= np.zeros(nb)

    if (f > mat):
        mat_vect[1]=mat
    else :
        for i in range(0,nb):
            mat_vect[i]=(i+1)*f

    return cf_vect, mat_vect 


















