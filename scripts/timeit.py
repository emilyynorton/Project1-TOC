import os
import sys
import matplotlib.pyplot as plt

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.sat import SatSolver
from src.helpers.dmaics_parser import parse_multi_instance_dimacs

dir_path = os.path.join(project_root, "input")
files = os.listdir(dir_path)

file = "kSAT2.cnf"
path = os.path.join(dir_path, file)
solver = SatSolver(path)
solver.run()

#################### GRAPH BRUTE FORCE ####################

# [[n_vars], [time_seconds], [satisfiable]]
points = [[],[],[]]

# Get the actual file names based on the naming convention used by save_results
results_dir = os.path.join(project_root, "results")
file_name_only = os.path.splitext(file)[0]  # "cnffile"
output_bf = os.path.join(results_dir, f"brute_force_{file_name_only}_sat_solver_results.csv")
output_btrack = os.path.join(results_dir, f"btracking_{file_name_only}_sat_solver_results.csv")

with open(output_bf) as f:
    next(f)  # Skip header line
    for line in f:
        components = line.strip().split(",")
        # print(components)
        points[0].append(int(components[1]))  # n_vars
        points[1].append(float(components[5]))  # time_seconds
        points[2].append(components[4].strip())  # satisfiable

print(points)
# Plot points with colors based on satisfiable status
for i in range(len(points[0])):
    color = 'green' if points[2][i] == 'S' else 'red'
    plt.scatter(points[0][i], points[1][i], c=color, s=50)

plt.xlabel('Number of Variables')
plt.ylabel('Time (seconds)')
plt.title('Brute Force SAT Solver Performance')
plt.show()

#################### GRAPH BACKTRACK ####################

# [[n_vars], [time_seconds], [satisfiable]]
points_btrack = [[],[],[]]

with open(output_btrack) as f:
    next(f)  # Skip header line
    for line in f:
        components = line.strip().split(",")
        # print(components)
        points_btrack[0].append(int(components[1]))  # n_vars
        points_btrack[1].append(float(components[5]))  # time_seconds
        points_btrack[2].append(components[4].strip())  # satisfiable

print(points_btrack)
# Plot points with colors based on satisfiable status
for i in range(len(points_btrack[0])):
    color = 'green' if points_btrack[2][i] == 'S' else 'red'
    plt.scatter(points_btrack[0][i], points_btrack[1][i], c=color, s=50)

plt.xlabel('Number of Variables')
plt.ylabel('Time (seconds)')
plt.title('Backtracking SAT Solver Performance')
plt.show()

# for file in files:
#     path = os.path.join(dir_path, file)