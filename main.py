from Data import Data
from GeneticAlgorithm import GeneticAlgorithm

data = Data("task.csv")
alg = GeneticAlgorithm(data)
alg.init(population=80, cross=30, stop_iters=30)
alg.solve()
alg.print_results()
