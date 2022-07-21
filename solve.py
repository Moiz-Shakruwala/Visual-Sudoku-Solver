#!/usr/bin/python3

from z3 import *
import argparse
import itertools
import time
from process import problem as pb

problem = pb

print("Problem Recieved: ")
for i in range(9):
    if i % 3 == 0 :
        print("|-------|-------|-------|")
    for j in range(9):
        if j % 3 == 0 :
            print ("|", end =" ")
        print(problem[i][j],end=" ")
    print("|")
print("|-------|-------|-------|")
print("\n-----------------------------\n solving...")

X = [[[Bool("X_%s_%s_%s"%(i+1,j+1,k+1))for i in range(9)]for j in range(9)]for k in range(9)]

nofvars = 0
def count():
	global nofvars
	rstring = nofvars
	nofvars +=1
	return str(rstring)

def get_fresh_vec(req_length):
	n_vs = []
	for i in range(req_length):
		n_vs.append( Bool( "b_" + count()))
	return n_vs

def sum_to_one( ls ):
    n= len(ls)
    aux = get_fresh_vec(n)
    F = [Or(Not(ls[0]),aux[0]),Or(ls[0],Not(aux[0])) ]
    for i in range(1,n):
        F+=[Or(Not(ls[i]),aux[i]), Or(Not(aux[i-1]),aux[i]), Or(Not(aux[i-1]),Not(ls[i])), Or(Not(aux[i]),aux[i-1],ls[i])]
    F+= [aux[n-1]]
    for i in range(n):
        F+=[]
    return F

Fs = []

# Encode already filled positions
for i in range(9):
    for j in range(9):
        if problem[i][j] !=0:
            k = problem[i][j]-1
            Fs += [X[i][j][k]]

# Encode for i,j  \sum_k x_i_j_k = 1
for i in range(9):
    for j in range(9):
        Fs+=sum_to_one(X[i][j][:])
# Encode for j,k  \sum_i x_i_j_k = 1
for j in range(9):
    for k in range(9):
        Y=[]
        for i in range(9):
            Y += [X[i][j][k]] 
        Fs+=sum_to_one(Y)
# Encode for i,k  \sum_j x_i_j_k = 1
for i in range(9):
    for k in range(9):
        Y=[]
        for j in range(9):
            Y += [X[i][j][k]] 
        Fs+=sum_to_one(Y)


s = Solver()
s.add( And( Fs ) )

if s.check() == sat:
    m = s.model()
    for i in range(9):
        if i % 3 == 0 :
            print("|-------|-------|-------|")
        for j in range(9):
            if j % 3 == 0 :
                print ("|", end =" ")
            for k in range(9):
                val = m[X[i][j][k]]
                if is_true( val ):
                    print("{}".format(k+1), end =" ")
        print("|")
    print("|-------|-------|-------|")
else:
    print("sudoku is unsat")

# print vars
