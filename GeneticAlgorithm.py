import numpy as np
import random
from copy import deepcopy

class GeneticAlgorithm:
    def __init__(self, data):
        self.data = data
        self.population = None
        self.n_population = None
        self.n_cross = None
        self.stop_iters = None

    def init(self, population=100, cross=50, stop_iters=20):
        """
        Generates the initial population
        :param population: number of individuals in the initial population
        :param cross: number of individuals crossed with each other
        :param stop_iters: the solver will stop if the cost is has not been improved in stop_iters iterations
        """

        self.stop_iters = stop_iters
        self.n_population = population
        self.population = [Genotype(data=self.data) for i in range(self.n_population)]
        if cross % 2 != 0:
            raise Exception("cross=%s must be an even number!" % (cross))
        elif cross > population:
            raise Exception("cross=%s must be less or equal to population=%s!" % (cross, population))

        self.n_cross = cross

    def solve(self):
        """
        Attempts to solve the problem
        """

        k = 0
        stop_i = 0
        min_cost = -1
        while stop_i < self.stop_iters:
            # Generate the even population of individuals to be crossed
            ind = [deepcopy(random.choice(self.population)) for i in range(self.n_cross)]

            # Cross the individuals in pairs
            for i in range(0, self.n_cross, 2):
                # Cross the two individuals
                ind[i].cross(ind[i + 1])
                ind[i].mutate()
                ind[i+1].mutate()

            # Add the new individuals to the pool
            self.population += ind

            # Sort the individuals by cost
            temp = np.zeros(self.n_population + self.n_cross, dtype=[('i', int), ('cost', float)])
            for idx, ind in enumerate(self.population):
                temp[idx] = (idx, ind.cost())

            temp.sort(order='cost')
            # Get indexes of individuals that should be removed from the population
            del_idxs = sorted(temp['i'][-self.n_cross:], reverse=True)
            for idx in del_idxs:
                del self.population[idx]

            # Get the minimal cost
            if temp['cost'][0] == min_cost:
                stop_i += 1
            else:
                min_cost = temp['cost'][0]

            print("Population: %s, cost: %s" % (k, min_cost))
            k += 1

    def print_results(self):
        """
        Prints the best solution
        """

        pass  # TODO


class Genotype:
    def __init__(self, data):
        """
        Constuctor - generates a random genotype
        :param data: The problem data source
        """

        self.data = data
        self.genes = self.data.get_random_genotype()

    def display(self):
        """
        Displays genotype's genes and total cost of the associated path
        """

        print("G: %s, Cost: %s" % (self.genes, self.cost()))

    def cost(self):
        """
        Calculates the total cost of the path represented by the genotype
        :return: Total cost of the path
        """

        # Store the remaining mass to be distributed
        remaining_mass = self.data.masses_sum

        # Calculate the cost from the start city to the first on in the genotype
        cost = self.section_cost(self.data.city_dists[self.genes[0]], remaining_mass)

        # Sum the costs on all sections
        for i, gene in enumerate(self.genes[0:-1]):
            remaining_mass -= self.data.masses[i]
            dist = self.data.adjM[gene, self.genes[i + 1]]
            cost += self.section_cost(dist, remaining_mass)

        # Add the cost of returning to the start city
        cost += self.section_cost(self.data.city_dists[self.genes[-1]], 0)

        return cost

    def section_cost(self, dist, mass):
        """
        Calculates the cost of given mass distribution on a given section of the path
        :param dist: Length of the section
        :param mass: Total mass distributed on the section
        :return: 
        """

        return (self.data.m_a * mass + self.data.m_b) * dist

    def cross(self, other):
        """
        Functions crosses the genotype with the other one
        :param other: The other genotype used in the crossing process
        :return: The output (crossed) genotype
        """

        # Generate a random locus (the index of division for the genotypes)
        locus = np.random.randint(1, self.data.N - 1)

        # Divide the genotypes into 2 pieces
        self1 = self.genes[:locus]
        self2 = self.genes[locus:]
        other1 = other.genes[:locus]
        other2 = other.genes[locus:]

        # Get the genes that will be missing
        miss1 = np.setdiff1d(self2, other2)
        miss2 = np.setdiff1d(other2, self2)

        # Replace the repeating values with the missing ones
        for m1, m2 in zip(miss1, miss2):
            np.place(other2, other2 == m2, m1)
            np.place(self2, self2 == m1, m2)

        # Cross and connect the pieces
        out1 = np.append(self1, other2)
        out2 = np.append(other1, self2)

        # Update the genotypes
        self.genes = out1
        other.genes = out2

    def mutate(self):
        """
        Performs a single mutation of the genotype
        :return: 
        """

        # Swap two neighbour genes at a random location (locus)
        locus = np.random.randint(1, self.data.N - 1)
        temp = self.genes[locus]
        self.genes[locus] = self.genes[locus + 1]
        self.genes[locus + 1] = temp