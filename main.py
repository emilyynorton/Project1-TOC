from src import entrypoint
from src.sat import SatSolver

def main():
    input_file = "input/kSAT.cnf"
    solver = SatSolver(input_file)
    solver.run()


if __name__ == "__main__":
    entrypoint.main()
