import random
from typing import List
from models.drone import Drone
from models.delivery_point import DeliveryPoint

class GeneticAlgorithm:
    def __init__(self, deliveries: List[DeliveryPoint], population_size=20, generations=50):
        self.deliveries = deliveries
        self.population_size = population_size
        self.generations = generations

    def create_individual(self) -> List[int]:
        indices = list(range(len(self.deliveries)))
        random.shuffle(indices)
        return indices

    def create_population(self) -> List[List[int]]:
        return [self.create_individual() for _ in range(self.population_size)]

    def fitness(self, individual: List[int]) -> float:
        total_priority = 0
        for i in individual:
            total_priority += self.deliveries[i].priority
        return total_priority

    def selection(self, population: List[List[int]]) -> List[List[int]]:
        population.sort(key=self.fitness, reverse=True)
        return population[:int(self.population_size * 0.5)]

    def crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        half = len(parent1) // 2
        child = parent1[:half]
        child += [x for x in parent2 if x not in child]
        return child

    def mutate(self, individual: List[int], mutation_rate=0.1):
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                j = random.randint(0, len(individual) - 1)
                individual[i], individual[j] = individual[j], individual[i]

    def run(self) -> List[int]:
        population = self.create_population()
        for _ in range(self.generations):
            selected = self.selection(population)
            children = []
            while len(children) < self.population_size:
                p1, p2 = random.sample(selected, 2)
                child = self.crossover(p1, p2)
                self.mutate(child)
                children.append(child)
            population = children
        best = max(population, key=self.fitness)
        return best

