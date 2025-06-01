# genetic_algorithm.py
import random
import numpy as np
from typing import List, Tuple
import copy

class GeneticAlgorithm:
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.1, generations: int = 100):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = []
        self.best_fitness_history = []
    
    def calculate_fitness(self, routes: List[List[int]], drones, deliveries, no_fly_zones) -> float:
        """
        Fitness hesaplama fonksiyonu
        Yüksek teslimat sayısı ödüllendirilir, yüksek enerji tüketimi ve kural ihlalleri cezalandırılır
        """
        completed_deliveries = 0
        total_energy = 0
        rule_violations = 0
        
        for drone_idx, route in enumerate(routes):
            if drone_idx >= len(drones) or not route:
                continue
                
            drone = drones[drone_idx]
            current_pos = drone['start_pos']
            current_weight = 0
            energy_consumed = 0
            
            for delivery_id in route:
                if delivery_id >= len(deliveries):
                    continue
                    
                delivery = deliveries[delivery_id]
                
                # Ağırlık kontrolü
                if current_weight + delivery['weight'] > drone['max_weight']:
                    rule_violations += 1
                    continue
                
                # Mesafe hesaplama
                distance = np.sqrt((delivery['pos'][0] - current_pos[0])**2 + 
                                 (delivery['pos'][1] - current_pos[1])**2)
                
                # Enerji tüketimi (basit model)
                energy_needed = distance * (1 + delivery['weight'] * 0.1)
                
                if energy_consumed + energy_needed <= drone['battery']:
                    completed_deliveries += 1
                    current_weight += delivery['weight']
                    energy_consumed += energy_needed
                    current_pos = delivery['pos']
                else:
                    rule_violations += 1
            
            total_energy += energy_consumed
        
        # Fitness hesaplama
        fitness = (completed_deliveries * 100) - (total_energy * 0.1) - (rule_violations * 1000)
        return max(fitness, 0)  # Negatif fitness'ı önle
    
    def create_individual(self, num_drones: int, num_deliveries: int) -> List[List[int]]:
        """Rastgele bir birey (rota kombinasyonu) oluştur"""
        individual = [[] for _ in range(num_drones)]
        deliveries = list(range(num_deliveries))
        random.shuffle(deliveries)
        
        # Teslimatları rastgele drone'lara dağıt
        for delivery_id in deliveries:
            drone_idx = random.randint(0, num_drones - 1)
            individual[drone_idx].append(delivery_id)
        
        return individual
    
    def initialize_population(self, num_drones: int, num_deliveries: int):
        """İlk popülasyonu oluştur"""
        self.population = []
        for _ in range(self.population_size):
            individual = self.create_individual(num_drones, num_deliveries)
            self.population.append(individual)
    
    def selection(self, fitness_scores: List[float]) -> Tuple[List[List[int]], List[List[int]]]:
        """Tournament selection ile ebeveyn seçimi"""
        def tournament_select():
            tournament_size = 3
            tournament_indices = random.sample(range(len(self.population)), tournament_size)
            tournament_fitness = [fitness_scores[i] for i in tournament_indices]
            winner_idx = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
            return self.population[winner_idx]
        
        parent1 = tournament_select()
        parent2 = tournament_select()
        return parent1, parent2
    
    def crossover(self, parent1: List[List[int]], parent2: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        """İki ebeveynden çocuk oluştur"""
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)
        
        # Basit crossover: rastgele drone'ları değiştir
        if len(child1) > 1 and len(child2) > 1:
            crossover_point = random.randint(0, len(child1) - 1)
            child1[crossover_point], child2[crossover_point] = child2[crossover_point], child1[crossover_point]
        
        return child1, child2
    
    def mutate(self, individual: List[List[int]]):
        """Bireyde mutasyon yap"""
        if random.random() < self.mutation_rate:
            # Rastgele bir teslimatı farklı bir drone'a taşı
            non_empty_drones = [i for i, route in enumerate(individual) if route]
            if len(non_empty_drones) >= 2:
                from_drone = random.choice(non_empty_drones)
                to_drone = random.randint(0, len(individual) - 1)
                
                if individual[from_drone]:
                    delivery = individual[from_drone].pop(random.randint(0, len(individual[from_drone]) - 1))
                    individual[to_drone].append(delivery)
    
    def optimize(self, drones, deliveries, no_fly_zones) -> Tuple[List[List[int]], float, List[float]]:
        """Genetic Algorithm ile optimizasyon"""
        print(f"🧬 GA Parametreleri: Popülasyon={self.population_size}, Mutasyon={self.mutation_rate}, Nesil={self.generations}")
        
        # İlk popülasyonu oluştur
        self.initialize_population(len(drones), len(deliveries))
        self.best_fitness_history = []
        
        best_individual = None
        best_fitness = -float('inf')
        
        for generation in range(self.generations):
            # Fitness hesapla
            fitness_scores = []
            for individual in self.population:
                fitness = self.calculate_fitness(individual, drones, deliveries, no_fly_zones)
                fitness_scores.append(fitness)
            
            # En iyi bireyi güncelle
            max_fitness = max(fitness_scores)
            if max_fitness > best_fitness:
                best_fitness = max_fitness
                best_individual = copy.deepcopy(self.population[fitness_scores.index(max_fitness)])
            
            self.best_fitness_history.append(best_fitness)
            
            # İlerleme göster
            if generation % 20 == 0 or generation == self.generations - 1:
                print(f"   Nesil {generation}: En iyi fitness = {best_fitness:.2f}")
            
            # Yeni nesil oluştur
            new_population = []
            
            # En iyi bireyi koru (elitism)
            new_population.append(copy.deepcopy(best_individual))
            
            # Geri kalan popülasyonu oluştur
            while len(new_population) < self.population_size:
                parent1, parent2 = self.selection(fitness_scores)
                child1, child2 = self.crossover(parent1, parent2)
                
                self.mutate(child1)
                self.mutate(child2)
                
                new_population.extend([child1, child2])
            
            # Popülasyon boyutunu ayarla
            self.population = new_population[:self.population_size]
        
        return best_individual, best_fitness, self.best_fitness_history