from Data import Data
from GeneticAlgorithm import GeneticAlgorithm
import matplotlib.pyplot as plt

data = Data("task.csv")
# data.disconnectCities("Bydgoszcz", "Gdynia")

#alg = GeneticAlgorithm(data)
#alg.init(population=80, cross=30, stop_iters=30)
#alg.solve()
#alg.print_results()

alg1 = GeneticAlgorithm(data)
alg1.init(population=100, cross=50, stop_iters=30)
alg1.solve()
alg1.print_results()

data.disconnectCities("Katowice", "Kraków")
data.disconnectCities("Siedlce", "Suwałki")
alg2 = GeneticAlgorithm(data)
alg2.init(population=100, cross=50, stop_iters=30)
alg2.solve()
alg2.print_results()

data.disconnectCities("Szczecin", "Poznań")
data.disconnectCities("Gliwice", "Katowice")
alg3 = GeneticAlgorithm(data)
alg3.init(population=100, cross=50, stop_iters=30)
alg3.solve()
alg3.print_results()

plt.plot(alg1.plt_x, alg1.plt_y, 'r-',alg2.plt_x, alg2.plt_y, 'b-',alg3.plt_x, alg3.plt_y, 'g-')
plt.title("Minimalny koszt w kolejnych populacjach")
plt.xlabel("Numer populacji")
plt.ylabel("Koszt minimalny [zł]")
plt.grid(True)
plt.show()
