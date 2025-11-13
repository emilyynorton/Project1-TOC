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
        # Create recursive function 
        def backtrack(assignment):
            all_satisfied = True
            for clause in clauses:
                clause_satisfied = False    # If clause is true
                undecided = False           # If there are unassigned vars in clause
                for literal in clause:
                    var = abs(literal)

                    # If the variable hasn't been assigned, make undecided true
                    if var not in assignment:
                        undecided = True
                        continue
                    
                    # Check the literal w/ curr assignment
                    val = assignment[var]
                    if (literal > 0 and val) or (literal < 0 and not val):
                        clause_satisfied = True
                        break
                
                # If all vars have been assigned and not satisfied, return False
                if not clause_satisfied:
                    if not undecided:
                        return False, {}
                    all_satisfied = False

            # Base case -- when all satisfied
            if all_satisfied:
                return True, assignment.copy()
            
            # Find next unassigned variable
            next_var = None
            for var in range(1, n_vars + 1):
                if var not in assignment:
                    break
                else:
                    return False, {}

            for val in [True, False]:
                assignment[var] = val
                found, sol = backtrack(assignment)
                if found:
                    return True, sol
                del assignment[var]
            
            return False, {}

        return backtrack({})

    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        # create all possible combinations of True, False corresponding to the number of variables in SAT problem
        boolean_combos = itertools.product([True, False], repeat=n_vars)

        # extract set of variables from problem (using set removes duplicates and sorted creates consistent list)
        all_variables = sorted(set(abs(literal) for clause in clauses for literal in clause))

        # check each set of T/F assignments
        for booleans in boolean_combos:
            # assign T/F to variable in SAT problem
            # store in variable assignments dictionary with variable name as key
            variable_assignments = {}
            for index, var in enumerate(all_variables):
                variable_assignments[var] = booleans[index]
                
            # start by assuming all clauses in SAT problem are true
            all_satisfied = True

            # check if each individual clause is true
            for clause in clauses:
                # start by assuming individual clause is false
                clause_satisfied = False
                # check each literal
                for literal in clause:
                    # get T/F assignment from variable assignments dictionary
                    # var is T and var is not negative = T
                    # var is F and var is negative = -F = T
                    if (variable_assignments[abs(literal)] and literal > 0) or (not variable_assignments[abs(literal)] and literal < 0):
                        # as soon as one literal in a clause is true, the whole clause is true because CNF uses "or" within clauses
                        clause_satisfied = True
                        break # go to next clause
            
                # case where no variable in the clause is true
                if clause_satisfied == False:
                    # clauses are connected by "and" in CNF, so if one clause is false, the whole statement is false
                    all_satisfied = False
                    break
  
            # if a solution was found, return solution
            if all_satisfied == True:
                return True, variable_assignments.copy()

        # no solution found
        return False, {}




    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass