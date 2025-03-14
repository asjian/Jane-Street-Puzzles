import random
import math
import numpy as np
import scipy

from scipy.integrate import quad
from scipy.optimize import minimize

def simulate(d, n):
    Awins = 0
    d_assume = 0.5

    for i in range(n):
        #Flag placement
        r = math.sqrt(random.uniform(0, 1))
        theta = random.uniform(0, 1) * 2 * math.pi
        Fx = r*math.cos(theta)
        Fy = r*math.sin(theta)

        #Aaron chooses value of rA to use
        rA = 0
        if d_assume <= 2*r:
            rA = math.sqrt(d_assume*(2*r-d_assume))
            '''
            if d <= r:
                rA = (d+1)/2.0
            else:
                rA = d/2.0
            '''

        #simulation of results of choices
        thetaA = random.uniform(0, 1) * 2 * math.pi
        Ax = rA*math.cos(thetaA)
        Ay = rA*math.sin(thetaA)

        dE = abs(d - r)
        dA = math.sqrt((Ax - Fx)**2 + (Ay - Fy)**2)

        if dA < dE:
            Awins += 1
        elif dA == dE:
            Awins += 0.5

    print(Awins/n)

d2 = 0.61

def integrand2(R, d):
    qty = min(1, max((d*(2*R - d) + 2*R*d - d**2)/(2*R*math.sqrt(d*(2*R-d))), -1.0))

    if abs(qty) > 1:
        print(d)
        print(R)
        print(qty)

    return R*math.acos(qty)

def integrand(R, d):
    qty = min(1, max((d2*(2*R - d2) + 2*R*d - d**2)/(2*R*math.sqrt(d2*(2*R-d2))), -1.0))

    if abs(qty) > 1:
        print(d)
        print(R)
        print(qty)

    return R*math.acos(qty)

def compute_integral(d):
    result, error = quad(lambda R: integrand(R, d), d2/2.0, 1)
    return result

def compute_integral_2(d):
    result, error = quad(lambda R: integrand2(R, d), d/2.0, 1)
    return result

def objective_function(d):
    return d2**2/4.0 + (2.0/math.pi)*compute_integral(d)

def objective_function_2(d):
    return d**2/4.0 + (2.0/math.pi)*compute_integral(d)

R = 0.3
d = 0.5
def objective_function_3(r):
    qty = max(min((r**2 + 2*R*d - d**2)/(2*r*R), 1.0), -1.0)
    return -1000*math.acos(qty)/math.pi

def og_objective_function(d):
    return d**2/4.0 + (2.0/math.pi)*compute_integral_2(d)

d0 = (d2 + 1)/2.0
d0_2 = (d2)/2.0

# Constraint to ensure that d is between 0 and 1 (since R goes from d to 1)
bounds = [(d2, 1)]
bounds2 = [(0, d2)]

'''
#result = minimize(objective_function, d0, method='L-BFGS-B', bounds=bounds, options={'disp': True, 'maxfun': 10000}, tol = 1e-20)
print()
result2 = minimize(objective_function_2, d0_2, method='L-BFGS-B', bounds=bounds2, options={'disp': True, 'maxfun': 10000}, tol = 1e-20)
print()
result3 = minimize(objective_function_3, R, method='SLSQP', bounds = [(0, 1)], options={'disp': True, 'maxfun': 100000}, tol = 1e-50)
print()
'''
result4 = minimize(og_objective_function, 0.5, method='L-BFGS-B', bounds=[(0, 1)], options={'disp': True, 'ftol': 1e-50}, tol = 1e-20)
print()

'''
print()
print("Optimal d, d > d':", result.x)
print("Minimum value of objective function (d > d'):", result.fun)
print()
print("Optimal d, d < d':", result2.x)
print("Minimum value of objective function (d < d'):", result2.fun)
print()
print("Optimal r, 0 < r < 1:", result3.x)
print("Maximum value of objective function (r):", -1*result3.fun)
print()
'''
print("Optimal d, 0 < d < 1:", result4.x)
print("Maximum value of objective function (d, original):", result4.fun)

print(og_objective_function(result4.x[0]))
print(og_objective_function(0.5))
#simulate(0.5, 1000000)
    
