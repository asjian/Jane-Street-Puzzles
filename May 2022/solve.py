from math import comb
from scipy.optimize import fsolve, brentq, minimize
import numpy as np
import matplotlib.pyplot as plt

def pdiscrete(pd):
  N = 23
  K = 7

  p = [[0 for k in range(K + 1)] for n in range(N + 1)]
  p[1][1] = 1

  for n in range(2, N + 1):
    for k in range(1, min(n + 1, K + 1)):
      p[n][k] = k / K * p[n - 1][k] + (K + 1 - k) / K * p[n - 1][k - 1]

  pwd = 0
  for n in range(24):
    pnd = pd**n*(1-pd)**(23-n)*comb(23,n)
    pwn = 0

    for i in range(n+1):
      p8 = (1/8)**(n-i)*(7/8)**i*comb(n,i)
      p0 = 0

      if n <= 16:
        p0 = 0

      elif i == 0:
        p0 = (n-16)/(2*n-23)

      else:
        for k in range(1, 8):
          p0 += p[i][k] * max(n-k-16,0)/(n-k)

      pwn += (p8/(n+1-i) * (1 + (n-i)*p0))

    pwd += pnd*pwn

  return pwd

def psplit(pd):
  N = 23
  K = 8
  p = [[0 for k in range(K + 1)] for n in range(N + 1)]
  p[1][1] = 1
  for n in range(2, N + 1):
    for k in range(1, min(n + 1, K + 1)):
      p[n][k] = k / K * p[n - 1][k] + (K + 1 - k) / K * p[n - 1][k - 1]

  pws = (1-pd)**23/3
  for n in range(1, 24):
    pn = pd**n*(1-pd)**(23-n)*comb(23,n)
    pwn = 0

    for k in range(1, 9):
      pwn += p[n][k] * min((8-k)/(24-n), 1)

    pws += pn * pwn

  return pws

guess = 0.95
solution = fsolve(lambda x: psplit(x) - pdiscrete(x), guess)
print(solution)
print(pdiscrete(solution), psplit(solution))

  
