import numpy as np
import csv
from geopy.distance import great_circle

class Data:
    def __init__(self, filename):
        # Load the cities database
        self.cities_db = {}
        with open('cities.csv', encoding='utf-8-sig') as csvcities:
            cityreader = csv.reader(csvcities, delimiter=';', quotechar='\"')
            for city in cityreader:
                self.cities_db[city[0]] = [float(city[1]), float(city[2])]

                self.start_city = None

        # Load the task
        self.visited_cities = []
        with open(filename, encoding='utf-8-sig') as csvtask:
            cityreader = csv.reader(csvtask, delimiter=';', quotechar='\"')
            for visit in cityreader:
                if self.start_city is None:
                    self.start_city = visit[0]
                else:
                    self.visited_cities.append([visit[0], float(visit[1])])

        # The number of cities visited
        self.N = len(self.visited_cities)

        # Calculate distances from the start city to the other cities
        self.city_dists = np.zeros(self.N)
        for idx, city in enumerate(self.visited_cities):
            self.city_dists[idx] = self.distance(self.start_city, city[0])

        # Names of the cities'
        self.city_names = [self.visited_cities[i][0] for i in range(self.N)]

        # Calculate the adjacency matrix of the cities graph
        self.adjM = np.zeros([self.N]*2)
        for i, src in enumerate(self.city_names):
            for j, dst in enumerate(self.city_names):
                if i != j:
                    self.adjM[i, j] = self.distance(src, dst)

        # The distributed masses
        self.masses = np.array([self.visited_cities[i][1] for i in range(self.N)])

        # Mass transportation cost parameters (cost(mass, distance) = (m_a*mass + m_b) * distance)
        self.m_a = 0.01/100.0*5.0 # 0.01 l/kg / 100 km * 5 zl/l
        self.m_b = 10.0/100.0*5.0 # 10.0 l / 100 km * 5 zl/l

        # Calculate the sum of distributed masses
        self.masses_sum = np.sum(self.masses)

    def distance(self, city1, city2):
        """
        Calculates the distance between two cities 
        :param city1: city1 name
        :param city2: city2 name
        :return: distance in km
        """

        return great_circle(self.cities_db[city1], self.cities_db[city2]).kilometers

    def get_random_genotype(self):
        """
        Returns a random genotype that represents a given route
        :return: random genotype
        """
        return np.random.permutation(self.N)

    def disconnectCities(self, city1, city2):
        i = None
        j = None
        if self.start_city == city1:
            try:
                j = self.city_names.index(city2)
            except(ValueError):
                print("Podane miasto '%s' nie istnieje!" % city2)
                return
            self.city_dists[j] = float("inf")
        elif self.start_city == city2:
            try:
                i = self.city_names.index(city1)
            except(ValueError):
                print("Podane miasto '%s' nie istnieje!" % city1)
                return
            self.city_dists[i] = float("inf")
        else:
            try:
                i = self.city_names.index(city1)
            except(ValueError):
                print("Podane miasto '%s' nie istnieje!" % city1)
                return
            try:
                j = self.city_names.index(city2)
            except(ValueError):
                print("Podane miasto '%s' nie istnieje!" % city2)
                return

        self.adjM[i, j] = float("inf")
        self.adjM[j, i] = float("inf")