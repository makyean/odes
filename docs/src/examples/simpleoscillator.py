# Authors: B. Malengier
"""
This example shows the most simple way of using a solver.
We solve free vibration of a simple oscillator::
        m \ddot{u} + k u = 0, u(0) = u_0, \dot{u}(0) = \dot{u}_0
using the IDA solver, which means we use residuals.
Solution::
        u(t) = u_0*cos(sqrt(k/m)*t)+\dot{u}_0*sin(sqrt(k/m)*t)/sqrt(k/m)

"""
from __future__ import print_function
from numpy import cos, sin, sqrt

#data
k = 4.0
m = 1.0
#initial data on t=0, x[0] = u, x[1] = \dot{u}, xp = \dot{x}
initx = [1, 0.1]
initxp = [initx[1], -k/m*initx[0]]

#define function for the residual equations which has specific signature
def reseqn(t, x, xdot, result):
    """ we create residual equations for the problem"""
    result[0] = m*xdot[1] + k*x[0]
    result[1] = xdot[0] - x[1]
    return 0

#instantiate the solver
from scikits.odes import dae

print ("Using the old api:")
solver = dae('ida', reseqn, old_api=True)
#obtain solution at a required time
result = solver.solve([0., 1., 2.], initx, initxp)
print('\n   t        Solution          Exact')
print('------------------------------------')
for t, u in zip(result[1], result[2]):
    print('%4.2f %15.6g %15.6g' % (t, u[0], initx[0]*cos(sqrt(k/m)*t)+initx[1]*sin(sqrt(k/m)*t)/sqrt(k/m)))

#continue the solver
result = solver.solve([result[1][-1], result[1][-1]+1], result[2][-1],
                      result[3][-1])

print('------------------------------------')
print('  ...continuation of the solution')
print('------------------------------------')
for t, u in zip(result[1], result[2]):
    print ('%4.2f %15.6g %15.6g' % (t, u[0], initx[0]*cos(sqrt(k/m)*t)+initx[1]*sin(sqrt(k/m)*t)/sqrt(k/m)))


print ("\nUsing the new api:")
solver = dae('ida', reseqn, old_api=False)
#obtain solution at a required time
result = solver.solve([0., 1., 2.], initx, initxp)
print('\n   t        Solution          Exact')
print('------------------------------------')
for t, u in zip(result.values.t, result.values.y):
    print('%4.2f %15.6g %15.6g' % (t, u[0], initx[0]*cos(sqrt(k/m)*t)+initx[1]*sin(sqrt(k/m)*t)/sqrt(k/m)))

#continue the solver
result = solver.solve([result.values.t[-1], result.values.t[-1]+1], result.values.y[-1],
                      result.values.ydot[-1])

print('------------------------------------')
print('  ...continuation of the solution')
print('------------------------------------')
for t, u in zip(result.values.t, result.values.y):
    print ('%4.2f %15.6g %15.6g' % (t, u[0], initx[0]*cos(sqrt(k/m)*t)+initx[1]*sin(sqrt(k/m)*t)/sqrt(k/m)))
