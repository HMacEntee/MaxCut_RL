# imports
import networkx as nx
import numpy as np
from typing import List, Union
from util import *
# PuLP is a linear & mixed integer programming modeler used to constuct 
# optimization problems and call solvers (CPLEX, GUROBI, etc...)
# https://coin-or.github.io/pulp/main/includeme.html
from pulp import *

# IMPORTANT 
# you must locally install the GUROBI and CPLEX solvers
# pip install gurobipy
# pip install cplex ???? doesnt work for me maybe you have to install it via gui at IBM Watson

# problem forumlation dervied from the below 
# https://www.tcs.tifr.res.in/~prahladh/teaching/2009-10/limits/lectures/lec03.pdf
def milp(graph, solver):

    # Create dictionary of weights dependent on weight/unweighted graph
    edges = graph.edges(data=True)
    weights = {}
    weighted = nx.is_weighted(graph)
    if weighted:
        pass
        weights ={(u, v) : w["weight"] for (u, v, w) in edges}
    else:
        weights = {(u, v) : 1 for (u, v, _) in edges}

    #define problem
    maxcut = LpProblem("maxcut", LpMaximize)

    # construct problem variables
    x = {node : pulp.LpVariable(name=f"x_{node}", cat="Binary") for node in graph.nodes}
    e = {(u, v): pulp.LpVariable(name=f"e_{u},{v}", cat="Binary") for (u, v, _) in edges}

    # define objective function
    maxcut += pulp.lpSum([weights[(u, v)] * e[(u, v)] for (u, v) in e]), "Sum_of_cut_edges"

    # define maxcut problem constraints
    for (u, v) in graph.edges:
        maxcut += (
            e[(u, v)] <= x[u] + x[v],
            f"cut_edge_constraint_three{u}_{v}"
        )
        maxcut += (
            e[(u, v)] <= 2 - (x[u] + x[v]),
            f"Ensure_cut_edge_principles_{u}_{v}"
        )
        
    # solve the problem using provided solver, adjuct time limit to graph size
    maxcut.solve(solver(msg=True, timeLimit=60))

    # display results
    print(f"Gurobi Status:{maxcut.status}")
    cutedges = [ pulp.value(e[(u, v)]) for (u, v) in e ]
    print(f"Edges cut: {sum(cutedges)}")

if __name__ == "__main__":

    # create temp nxgraph (weighted and unweighted)
    fiveGNW= nx.Graph()
    fiveGNW.add_nodes_from([0,1,2,3,4])
    fiveGNW.add_edges_from([(0,1), (0,2), (1,2), (1,3), (2,4), (3,4)])

    fiveGW= nx.Graph()
    fiveGW.add_nodes_from([0,1,2,3,4])
    fiveGW.add_weighted_edges_from([(0,1,1), (0,2,1), (1,2,1), (1,3,1), (2,4,1), (3,4,1)])

    # List available solvers usable locally
    print(listSolvers(onlyAvailable=True))

    # solve for undirected graph
    milp(fiveGNW, GUROBI)    
    # milp(fiveGNW, CPLEX)    
        




