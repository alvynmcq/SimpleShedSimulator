# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 11:28:19 2012

@author: anders
"""


import os

def make_register(Register_name):
    a=Register_name+'.txt'
    f = open(a, 'w')
    f
    f.write('ID,Category, Name, Impact, U_i, Prob, U_p, Risk owner, Mitigation, Contigation, Action by, Action when')
    f.write('\n')
    f.close()
   # print('New register created...')

def make_entry(ID, Category, Name, Impact, U_i, Prob, U_p, Risk_owner, Mitigation, Contigation, Action_by, Action_when):
    entry=ID+','+Category+','+ Name+','+ Impact+ ','+U_i+','+ Prob+','+ U_p+ ','+Risk_owner+','+ Mitigation+','+ Contigation+','+ Action_by+','+ Action_when+','
    return entry

def append_register(Register_name, entry):
    a=Register_name +'.txt'
    f = open(a, 'a')
    for q in entry:
        f.write(q)
    f.write('\n')
    f.close()
    #print('Entry appended...')

def read_register(Register_name):
    a=Register_name #+'.txt'
    f = open(a, 'r')
    register=[]
    for q in f.readlines():
        qq=q.split(',')
        qq.pop(len(qq)-1)
        register.append(qq)
    register.pop(0)
    return register

def delete_entry(Register_name, entry_ID):
    a=Register_name + '.txt'
    f = open(a, 'r')
    lines = f.readlines()
    f.close()
    f = open(a, 'w')
    for line in lines:
        if line[0] != entry_ID:
            f.write(line)
    f.close()

def make_factor_register(Register_name):
    ''' this functon looks for the risk register
        and makes a corresponding factor register.
        If the risk register does exist it skips the
        whole shablam...
    '''
    if os.path.isfile(Register_name):
        a=Register_name+'_factors'+'.txt'
        f = open(a, 'w')
        f.write('ID,Uncertainty,Mean_Uncertainty,EX,Mean_EX,P_s, Mean_P_s')
        f.write('\n')
        f.close()

def append_risk_factor(Register_name,ID,Uncertainty,EX,P_s):
    '''This function opens the factor register
    and append a risk factors to selected ID.
    If the factor register does not exist, 
    one will be created
    '''
    if os.path.isfile(Register_name):
        a=Register_name+'_factors'+'.txt'
        if os.path.isfile(a):
            mean_uncertainty=sum(Uncertainty)/len(Uncertainty)          
            mean_EX=sum(EX)/len(EX)          
            mean_P_s=sum(P_s)/len(P_s)
            factors=str(ID)+','+str(Uncertainty)+','+str(mean_uncertainty)+','+str(EX)+','+str(mean_EX)+','+str(P_s)+','+str(mean_P_s)     
            f = open(a, 'a')
            f.write(factors)
            f.write('\n')
            f.close()
        else:
           make_factor_register(Register_name) 
           mean_uncertainty=sum(Uncertainty)/len(Uncertainty)          
           mean_EX=sum(EX)/len(EX)          
           mean_P_s=sum(P_s)/len(P_s)
           factors=str(ID)+','+str(Uncertainty)+','+str(mean_uncertainty)+','+str(EX)+','+str(mean_EX)+','+str(P_s)+','+str(mean_P_s)     
           f = open(a, 'a')
           f.write(factors)
           f.write('\n')
           f.close()


append_risk_factor(Register_name='ggg.txt',ID=1,Uncertainty=[1, 2, 3, 4, 5],EX=[1, 2, 3, 4, 5],P_s=[6, 7, 8, 9, 10])




