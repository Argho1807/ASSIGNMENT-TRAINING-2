""" N-QUEENS PROBLEM """

import gurobipy as gp
import pandas as pd
from gurobipy import GRB

class Optimiser():
    def __init__(self):
        # self.diagonaltraversal()
        self.inputparams()
        self.optmodel()
        self.variables()
        self.constraints()
        # self.objective()
        self.solve()
        self.printoutputs()

    def diagonaltraversal(self):
        str1, str2, str3, str4 = "[", "[", "[", "["
        for k in range(8):
            str1 += ", [" if k > 0 else ""
            str2 += ", [" if k > 1 else ""
            str3 += ", [" if k > 0 else ""
            str4 += ", [" if k > 1 else ""
            for j in range(0, k+1):
                str1 += ", " if j > 0 else ""
                str3 += ", " if j > 0 else ""
                row, col = j, k-j
                str1 += f"({row},{col})"
                row, col = 7+j-k, j
                str3 += f"({row},{col})"
            if k > 0:
                for j in range(0, 7-k+1):
                    str2 += ", " if j > 0 else ""
                    str4 += ", " if j > 0 else ""
                    row, col = j+k, 7-j
                    str2 += f"({row},{col})"
                    row, col = j, j+k
                    str4 += f"({row},{col})"
                str2 += "]"
                str4 += "]"
            str1 += "]"
            str3 += "]"

    def inputparams(self):
        self.gridsize = 8
        self.grid = [_ for _ in range(0, self.gridsize)]

    def optmodel(self):
        self.model = gp.Model("N-Queens")

    def variables(self):
        self.ifQueenSelected = self.model.addVars(self.grid, self.grid, vtype=GRB.BINARY, name=f"if_Queen_selected")

    def constraints(self):
        # row-wise, col-wise
        for idx in self.grid:
            self.model.addConstr(self.ifQueenSelected.sum(idx, "*") == 1, f"row_wise_{idx}")
            self.model.addConstr(self.ifQueenSelected.sum("*", idx) == 1, f"col_wise_{idx}")

        """ DIAGONAL TRAVERSALS """
        # 1 -
        # [(0,0)],
        # [(0,1), (1,0)],
        # [(0,2), (1,1), (2,0)],
        # [(0,3), (1,2), (2,1), (3,0)],
        # [(0,4), (1,3), (2,2), (3,1), (4,0)],
        # [(0,5), (1,4), (2,3), (3,2), (4,1), (5,0)],
        # [(0,6), (1,5), (2,4), (3,3), (4,2), (5,1), (6,0)],
        # [(0,7), (1,6), (2,5), (3,4), (4,3), (5,2), (6,1), (7,0)]

        for K in self.grid:
            self.model.addConstr(gp.quicksum(self.ifQueenSelected[J,K-J]
                                             for J in range(0, K+1))
                                 <= 1, f"diagonal_traversal_1.{K}")

        # 2 -
        # [(1,7), (2,6), (3,5), (4,4), (5,3), (6,2), (7,1)],
        # [(2,7), (3,6), (4,5), (5,4), (6,3), (7,2)],
        # [(3,7), (4,6), (5,5), (6,4), (7,3)],
        # [(4,7), (5,6), (6,5), (7,4)],
        # [(5,7), (6,6), (7,5)],
        # [(6,7), (7,6)],
        # [(7,7)]

        for K in self.grid[1:]:
            self.model.addConstr(gp.quicksum(self.ifQueenSelected[J+K, self.gridsize-1-J]
                                             for J in range(0, self.gridsize-1-K+1))
                                 <= 1, f"diagonal_traversal_2.{K}")

        # 3 -
        # [(7,0)]
        # [(6,0), (7,1)],
        # [(5,0), (6,1), (7,2)],
        # [(4,0), (5,1), (6,2), (7,3)],
        # [(3,0), (4,1), (5,2), (6,3), (7,4)],
        # [(2,0), (3,1), (4,2), (5,3), (6,4), (7,5)],
        # [(1,0), (2,1), (3,2), (4,3), (5,4), (6,5), (7,6)],
        # [(0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)]

        for K in self.grid:
            self.model.addConstr(gp.quicksum(self.ifQueenSelected[self.gridsize-1+J-K, J]
                                             for J in range(0, K+1))
                                 <= 1, f"diagonal_traversal_3.{K}")

        # 4 -
        # [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7)],
        # [(0,2), (1,3), (2,4), (3,5), (4,6), (5,7)],
        # [(0,3), (1,4), (2,5), (3,6), (4,7)],
        # [(0,4), (1,5), (2,6), (3,7)],
        # [(0,5), (1,6), (2,7)],
        # [(0,6), (1,7)],
        # [(0,7)]

        for K in self.grid[1:]:
            self.model.addConstr(gp.quicksum(self.ifQueenSelected[J, J+K]
                                             for J in range(0, self.gridsize-1-K+1))
                                 <= 1, f"diagonal_traversal_4.{K}")

    def objective(self):
        self.obj = self.ifQueenSelected.sum("*")

    def solve(self):
        # self.model.setObjective(self.obj, GRB.MINIMIZE)
        self.model.setParam('TimeLimit', 60)
        self.model.Params.PoolSearchMode = 2
        self.model.Params.PoolSolutions = 100
        self.model.optimize()

    def printoutputs(self):
        # if self.model.status not in [GRB.INFEASIBLE, GRB.UNBOUNDED, GRB.INF_OR_UNBD]:
        #     print("Optimal solution" if self.model.status == GRB.OPTIMAL else "Feasible solution")

        print(f"Number of solutions of N-Queens with {self.gridsize}*{self.gridsize} gridsize - {self.model.SolCount}")

        for i in range(min(100, self.model.SolCount)):
            self.model.setParam(GRB.Param.SolutionNumber, i)
            self.outputdf = pd.DataFrame([["Q" if self.ifQueenSelected[row, col].Xn > 0.1
                                           else "-" for col in self.grid] for row in self.grid]
                                         , columns=self.grid[1:]+[self.gridsize]
                                         , index=self.grid[1:]+[self.gridsize])

            print(f"\nsolution number - {i+1}\n")
            print(self.outputdf)

Optimiser()