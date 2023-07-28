# Assignment - Q1

import numpy as np
import pandas as pd
import time
from datetime import datetime

from ortools.linear_solver import pywraplp

# MODEL FORMULATION USING OR TOOLS

N = 8 # Chess board

# FORMULATION

# START TIME
start = time.time()
now = datetime.now()
print("\nStarted at -",now.strftime("%H:%M:%S"),'\n')

solver = pywraplp.Solver.CreateSolver('SCIP')
time_limit = 30 # in minutes
solver.SetTimeLimit(1000*60*time_limit) 

# DECISION VARIABLES
X = {(i,j): solver.IntVar(0, 1, f'X_{i}_{j}') for i in range(N) for j in range(N)} # 1 if cell (i,j) is occupied with a queen

# CONSTRAINTS

# 1 - Only one queen in each row
for i in range(N):
    solver.Add(solver.Sum([X[i,j] for j in range(N)]) == 1)

# 2 - Only one queen in each column
for j in range(N):
    solver.Add(solver.Sum([X[i,j] for i in range(N)]) == 1)

# 3 - At most one queen in each diagonal
for i in range(N):
    for j in range(N):
        solver.Add(solver.Sum([X[i+k, j+k] for k in range(min(N-i, N-j))]) <= 1)
        solver.Add(solver.Sum([X[i-k, j+k] for k in range(min(i+1, N-j))]) <= 1)

# OBJECTIVE
objective_function = [X[i,j] for i in range(N) for j in range(N)]

# SOLVER
solver.Minimize(solver.Sum(objective_function))
status = solver.Solve()

# OUTPUT

if status == pywraplp.Solver.OPTIMAL:
    #print('Objective value =', solver.Objective().Value())
    #print('Total number of variables =', solver.NumVariables())
    #print('Total number of constraints =', solver.NumConstraints())
    #print('Problem solved in %f milliseconds' % solver.wall_time())
    #print('Problem solved in %d iterations' % solver.iterations())
    #print('Problem solved in %d branch-and-bound nodes' % solver.nodes(),'\n')
    print('Chessboard with queens placed-\n')
    Q = [[0 for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(N):
            if round(X[i,j].solution_value(), 2) == 1:
                Q[i][j] = 'Q'
            else:
                Q[i][j] = '-'

    print(pd.DataFrame(Q, index = [i+1 for i in range(N)], columns = [j+1 for j in range(N)]))

else:
    print('The problem does not have an optimal solution.')

# END TIME
now = datetime.now()
print("\nEnded at -",now.strftime("%H:%M:%S"))
end = time.time()
print(f"Runtime of the program is {round(((end - start)/60),2)} minutes\n")