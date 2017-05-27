from Data import Data
from GeneticAlgorithm import GeneticAlgorithm

data = Data()
alg = GeneticAlgorithm(data)

alg.init(population=100, cross=4, stop_iters=10)
alg.solve()
# alg.print_results()