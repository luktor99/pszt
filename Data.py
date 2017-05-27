import numpy as np

class Data:
    def __init__(self):

        # SAMPLE DATA TODO: Load data from a file
        # The number of cities visited
        self.N = 5
        # Adjacency matrix of the cities graph
        self.adjM = np.matrix([[0, 3, 6, 9, 12],
                               [3, 0, 3, 6, 9],
                               [6, 3, 0, 3, 6],
                               [9, 6, 3, 0, 3],
                               [12, 9, 6, 3, 0]])
        # Distances from the start city to the other cities
        self.city_dists = np.array([5, 8, 11, 14, 17])
        # Names of the cities
        self.start_name = 'X'
        self.city_names = ['A', 'B', 'C', 'D', 'E']
        # The distributed masses
        self.masses = np.array([100]*self.N)

        # Mass transportation cost parameters (cost(mass, distance) = (m_a*mass + m_b) * distance)
        self.m_a = 0
        self.m_b = 1

        # Calculate the sum of distributed masses
        self.masses_sum = np.sum(self.masses)

    def get_random_genotype(self):
        """
        Returns a random genotype that represents a given route
        :return: random genotype
        """
        return np.random.permutation(self.N)