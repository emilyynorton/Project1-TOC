"""
SAT Solver - DIMACS-like Multi-instance Format
----------------------------------------------------------
Project 1: Tough Problems & The Wonderful World of NP

INPUT FORMAT (multi-instance file):
-----------------------------------
Each instance starts with a comment and a problem definition:

c <instance_id> <k> <status?>
p cnf <n_vertices> <n_edges>
u,v
x,y
...

Example:
c 1 3 ?
p cnf 4 5
1,2
1,3
2,3
2,4
3,4
c 2 2 ?
p cnf 3 3
1,2
2,3
1,3

OUTPUT:
-------
A CSV file named 'resultsfile.csv' with columns:
instance_id,n_vars,n_clauses,method,satisfiable,time_seconds,solution


EXAMPLE OUTPUT
------------
instance_id,n_vars,n_clauses,method,satisfiable,time_seconds,solution
3,4,10,U,0.00024808302987366915,BruteForce,{}
4,4,10,S,0.00013304100139066577,BruteForce,"{1: True, 2: False, 3: False, 4: False}"
"""

from typing import List, Tuple, Dict
from src.helpers.sat_solver_helper import SatSolverAbstractClass
import itertools


class SatSolver(SatSolverAbstractClass):

    """
        NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
        For this you dont need to save anything just make sure to return exact related output.
        
        For ease look at the Abstract Solver class and basically we are having the run method which does the saving
        of the CSV file just focus on the logic
    """

    def sat_backtracking(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        def backtrack(assignment):
            # Check if all clauses are satisfied
            all_satisfied = True
            for clause in clauses:
                clause_satisfied = False
                undecided = False
                for literal in clause:
                    var = abs(literal)
                    if var not in assignment:
                        undecided = True
                        continue
                    val = assignment[var]
                    if (literal > 0 and val) or (literal < 0 and not val):
                        clause_satisfied = True
                        break
                if not clause_satisfied:
                    if not undecided:
                        return False, {}
                    all_satisfied = False

            # If all satisfied return solution
            if all_satisfied:
                return True, assignment.copy()
            
            # Find 1st unassigned variable
            next_var = None
            for var in range(1, n_vars + 1):
                if var not in assignment:
                    next_var = var
                    break
            
            # If all vars assigned but not all clauses satisfied, return False
            if next_var is None:
                return False, {}

            # Try assigning true then false
            for val in [True, False]:
                assignment[next_var] = val
                found, sol = backtrack(assignment)
                if found:
                    return True, sol
                del assignment[next_var]
            
            return False, {}

        return backtrack({})

    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        boolean_combos = itertools.product([True, False], repeat=n_vars)
        # set removes duplicates
        # sorted makes it into a list for consistency
        all_variables = sorted(set(abs(literal) for clause in clauses for literal in clause))

        for booleans in boolean_combos:
            variable_assignments = {}
            for index, var in enumerate(all_variables):
                variable_assignments[var] = booleans[index]
                
            all_satisfied = True

            for clause in clauses:
                clause_satisfied = False
                for literal in clause:
                    if (variable_assignments[abs(literal)] and literal > 0) or (not variable_assignments[abs(literal)] and literal < 0):
                        clause_satisfied = True
                        break # go to next clause
                              # only one of the variables needs to be true because of the "or" in CNF
                              # True and -False evaluate to True
                              # as soon as you see one of those, that segment is true
                if clause_satisfied == False:
                    all_satisfied = False
                    break # as soon as one entire clause is false, the "and" makes the whole thing false
  
            if all_satisfied == True:
                return True, variable_assignments.copy()

        return False, {}




    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass