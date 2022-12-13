"""
I found methods in both libraries that solve the Least-squares problem and compare between them.
it can be seen that numpy runs faster.
helped by:
https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq
https://www.cvxpy.org/examples/basic/least_squares.html
"""

import matplotlib.pyplot as plt
import numpy as np
import cvxpy as cp
import time as tm


def cvxpy_solve(A, b): # from the example in the doc
    start_time = tm.time()
    x = cp.Variable(A.shape[1])
    objective = cp.Minimize(cp.sum_squares(A @ x - b))
    constraints = []
    prob = cp.Problem(objective, constraints)
    prob.solve()
    end_time = tm.time()
    return end_time - start_time

def numpy_solve(A, b): # from the example in the doc
    start_time = tm.time()
    x = np.linalg.lstsq(A, b)
    end_time = tm.time()
    return end_time - start_time

def rand_generator(len): # generate matrix and vector
    matr = np.random.rand(len, len)
    vect = np.random.rand(len)
    return matr, vect

def draw_diff(size, numpy_time, cvxpy_time):
    plt.plot(numpy_time, size, label='numpy')
    plt.plot(cvxpy_time, size, label='cvxpy')
    plt.xlabel('time')
    plt.ylabel('size')
    plt.legend()
    plt.show()


def run_test():
    size = []
    numpy_time = []
    cvxpy_time = []
    for i in range(50, 1000):
        matr, vect = rand_generator(i)
        size.append(i)
        time = numpy_solve(matr, vect)
        numpy_time.append(time)
        time = cvxpy_solve(matr, vect)
        cvxpy_time.append(time)
    draw_diff(size, numpy_time, cvxpy_time)

run_test()