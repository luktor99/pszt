from Data import Data
from GeneticAlgorithm import GeneticAlgorithm, Genotype

data = Data()
alg = GeneticAlgorithm(data)

alg.init(population=400, cross=10, stop_iters=2000)
alg.solve()
alg.print_results()