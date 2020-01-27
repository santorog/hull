#!/usr/bin/python3

import numpy as np
import scipy.optimize as sco
import utilities as ul
from functools import partial

### Evaluation des obligations, taux actuariel, taux au pair

# Bond 4-y, 3% per y
nom=100
zc=[0.025,0.029,0.032,0.034]
cf=[3,3,3,nom+3]
mat=[1,2,3,4]

def price(cf_c,zc_r, mat_r):
    value=0
    for i in range(len(cf_c)):
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

def cf_mat_zc_for_year(f, yearly_coupon, mat, nom, mat_t, zc_t):
    nb= max(1,int(mat/f))

    mat_vect= np.zeros(nb)
    zc_vect = np.zeros(nb)
    cf_vect = np.zeros(nb)

    if (f > mat):
        mat_vect[0]=mat
        zc_vect[0]=zc_t[0]
    else :
        cf_vect= np.full(nb, yearly_coupon * f)
        for i in range(nb):
            mat_vect[i]=(i+1)*f
            zc_vect[i] = zc_t[mat_t.index(mat_vect[i])] 

    cf_vect[-1]+= nom 

    return cf_vect, mat_vect, zc_vect


def bootstrap(nom_t, mat_t, cp_y_t, pv_t):

    size=len(mat_t)

    b_zc_r=np.zeros(size)

    def p_except_last(pv,cf,mat,val,r):
        return pv + cf*np.exp(-mat*r) - val

    for i in range(size):
        cf_vect, mat_vect, zc_vect = cf_mat_zc_for_year(b_f,b_cp_y[i],b_mat[i],b_nom[i],mat_t, b_zc_r)
        idx=len(cf_vect)-1

        print(i)
        print("CF ", cf_vect)
        print(" MAT: ", mat_vect)
        print("ZC : ",zc_vect)
        print("IDX : ",idx)

        pv= price(cf_vect[:idx],zc_vect[:idx],mat_vect[:idx])

        print("PV is : ", pv)
        H=partial(p_except_last, pv, cf_vect[idx], mat_vect[idx], pv_t[i])

        b_zc_r[i]= sco.broyden2(H,0.05)

    return b_zc_r


print(bootstrap(b_nom,b_mat,b_cp_y,b_pv))

