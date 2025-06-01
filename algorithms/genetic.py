# algorithms/genetic.py - FİNAL GÜNCELLENMİŞ VERSİYON
import random
import numpy as np
from typing import List, Tuple
import copy
from utils.geometry import calculate_distance

class GeneticAlgorithm:
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.1, generations: int = 100):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = []
        self.best_fitness_history = []

    def calculate_fitness(self, routes: List[List[int]], drones, deliveries, no_fly_zones) -> float:
        """
        İYİLEŞTİRİLMİŞ FITNESS FONKSIYONU
        Formül: (Teslimat sayısı × 100) - (Enerji × 0.5) - (Kural ihlali × 200)
        """
        completed_deliveries = 0
        total_energy = 0
        rule_violations = 0
        total_distance = 0
        no_fly_violations = 0

        for drone_idx, route in enumerate(routes):
            if drone_idx >= len(drones) or not route:
                continue

            drone = drones[drone_idx]
            current_pos = drone.start_pos
            current_weight = 0
            energy_consumed = 0
            route_distance = 0

            for delivery_id in route:
                if delivery_id >= len(deliveries):
                    continue

                delivery = deliveries[delivery_id]

                # 1. AĞIRLIK KONTROLÜ
                if current_weight + delivery.weight > drone.max_weight:
                    rule_violations += 1
                    continue

                # 2. MESAFE VE ENERJİ HESAPLAMA
                distance = calculate_distance(current_pos, delivery.pos)
                route_distance += distance
                
                # Gelişmiş enerji modeli: Uzaklık × (1 + ağırlık faktörü)
                energy_needed = distance * (1 + (current_weight + delivery.weight) * 0.1)

                # 3. BATARYA KONTROLÜ
                if energy_consumed + energy_needed <= drone.battery:
                    completed_deliveries += 1
                    current_weight += delivery.weight
                    energy_consumed += energy_needed
                    current_pos = delivery.pos
                    
                    # 4. NO-FLY ZONE KONTROLÜ
                    for no_fly_zone in no_fly_zones:
                        if no_fly_zone.does_path_intersect(drone.current_pos, delivery.pos):
                            no_fly_violations += 1
                else:
                    rule_violations += 1

            total_energy += energy_consumed
            total_distance += route_distance

        # FİTNESS HESAPLAMA - İYİLEŞTİRİLMİŞ FORMÜL
        delivery_reward = completed_deliveries * 100
        energy_penalty = total_energy * 0.5
        rule_penalty = rule_violations * 200  
        no_fly_penalty = no_fly_violations * 300
        distance_penalty = total_distance * 0.1

        fitness = delivery_reward - energy_penalty - rule_penalty - no_fly_penalty - distance_penalty
        return max(fitness, 0)

    def create_individual(self, num_drones: int, num_deliveries: int) -> List[List[int]]:
        """GELİŞMİŞ BAŞLANGIÇ POPÜLASYONU - Akıllı dağıtım"""
        individual = [[] for _ in range(num_drones)]
        deliveries = list(range(num_deliveries))
        random.shuffle(deliveries)

        # Teslimatları drone'lara dengeli dağıt
        for i, delivery_id in enumerate(deliveries):
            drone_idx = i % num_drones  # Round-robin dağıtım
            individual[drone_idx].append(delivery_id)

        # Her drone'un rotasını karıştır
        for route in individual:
            random.shuffle(route)

        return individual

    def initialize_population(self, num_drones: int, num_deliveries: int):
        """İlk popülasyonu oluştur - %20 akıllı, %80 rastgele"""
        self.population = []
        
        # %20 akıllı bireyler
        smart_count = max(1, self.population_size // 5)
        for _ in range(smart_count):
            individual = self.create_individual(num_drones, num_deliveries)
            self.population.append(individual)
        
        # %80 tamamen rastgele bireyler
        for _ in range(self.population_size - smart_count):
            individual = [[] for _ in range(num_drones)]
            deliveries = list(range(num_deliveries))
            random.shuffle(deliveries)

            for delivery_id in deliveries:
                drone_idx = random.randint(0, num_drones - 1)
                individual[drone_idx].append(delivery_id)
            
            self.population.append(individual)

    def selection(self, fitness_scores: List[float]) -> Tuple[List[List[int]], List[List[int]]]:
        """İYİLEŞTİRİLMİŞ TOURNAMENT SELECTION"""
        def tournament_select():
            tournament_size = min(5, len(self.population))  # Daha büyük turnuva
            tournament_indices = random.sample(range(len(self.population)), tournament_size)
            tournament_fitness = [fitness_scores[i] for i in tournament_indices]
            winner_idx = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
            return self.population[winner_idx]

        parent1 = tournament_select()
        parent2 = tournament_select()
        return parent1, parent2

    def crossover(self, parent1: List[List[int]], parent2: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        """GELİŞMİŞ CROSSOVER - Order Crossover (OX) benzeri"""
        child1 = [[] for _ in range(len(parent1))]
        child2 = [[] for _ in range(len(parent2))]

        # Tüm teslimatları topla
        all_deliveries_p1 = []
        all_deliveries_p2 = []
        
        for route in parent1:
            all_deliveries_p1.extend(route)
        for route in parent2:
            all_deliveries_p2.extend(route)

        # Crossover noktası belirle
        if all_deliveries_p1 and all_deliveries_p2:
            crossover_point = len(all_deliveries_p1) // 2
            
            # İlk yarıyı koru, ikinci yarıyı değiş
            combined1 = all_deliveries_p1[:crossover_point] + all_deliveries_p2[crossover_point:]
            combined2 = all_deliveries_p2[:crossover_point] + all_deliveries_p1[crossover_point:]
            
            # Tekrarları temizle
            combined1 = list(dict.fromkeys(combined1))  # Sırayı koruyarak tekrarları kaldır
            combined2 = list(dict.fromkeys(combined2))

            # Drone'lara yeniden dağıt
            for i, delivery in enumerate(combined1):
                drone_idx = i % len(child1)
                child1[drone_idx].append(delivery)
                
            for i, delivery in enumerate(combined2):
                drone_idx = i % len(child2)
                child2[drone_idx].append(delivery)
        else:
            child1 = copy.deepcopy(parent1)
            child2 = copy.deepcopy(parent2)

        return child1, child2

    def mutate(self, individual: List[List[int]]):
        """GELİŞMİŞ MUTASYON - 3 tip mutasyon"""
        if random.random() < self.mutation_rate:
            mutation_type = random.choice(['swap', 'insert', 'reverse'])
            
            if mutation_type == 'swap':
                self._swap_mutation(individual)
            elif mutation_type == 'insert':
                self._insert_mutation(individual)
            else:
                self._reverse_mutation(individual)

    def _swap_mutation(self, individual: List[List[int]]):
        """İki teslimatın yerini değiştir"""
        non_empty_drones = [i for i, route in enumerate(individual) if route]
        if len(non_empty_drones) >= 2:
            drone1, drone2 = random.sample(non_empty_drones, 2)
            
            if individual[drone1] and individual[drone2]:
                # İki teslimatı swap et
                idx1 = random.randint(0, len(individual[drone1]) - 1)
                idx2 = random.randint(0, len(individual[drone2]) - 1)
                
                individual[drone1][idx1], individual[drone2][idx2] = \
                    individual[drone2][idx2], individual[drone1][idx1]

    def _insert_mutation(self, individual: List[List[int]]):
        """Bir teslimatı başka drone'a taşı"""
        non_empty_drones = [i for i, route in enumerate(individual) if route]
        if non_empty_drones:
            from_drone = random.choice(non_empty_drones)
            to_drone = random.randint(0, len(individual) - 1)

            if individual[from_drone]:
                delivery = individual[from_drone].pop(
                    random.randint(0, len(individual[from_drone]) - 1)
                )
                individual[to_drone].append(delivery)

    def _reverse_mutation(self, individual: List[List[int]]):
        """Bir drone'un rotasının bir kısmını tersine çevir"""
        non_empty_drones = [i for i, route in enumerate(individual) if len(route) > 1]
        if non_empty_drones:
            drone_idx = random.choice(non_empty_drones)
            route = individual[drone_idx]
            
            if len(route) >= 2:
                start = random.randint(0, len(route) - 2)
                end = random.randint(start + 1, len(route))
                route[start:end] = reversed(route[start:end])

    def optimize(self, drones, deliveries, no_fly_zones) -> Tuple[List[List[int]], float, List[float]]:
        """GELİŞMİŞ GENETİK ALGORİTMA OPTİMİZASYONU"""
        print(f"🧬 GA Parametreleri: Popülasyon={self.population_size}, Mutasyon={self.mutation_rate}, Nesil={self.generations}")

        self.initialize_population(len(drones), len(deliveries))
        self.best_fitness_history = []

        best_individual = None
        best_fitness = -float('inf')
        stagnation_counter = 0
        max_stagnation = 20

        for generation in range(self.generations):
            fitness_scores = []
            for individual in self.population:
                fitness = self.calculate_fitness(individual, drones, deliveries, no_fly_zones)
                fitness_scores.append(fitness)

            current_max_fitness = max(fitness_scores)
            
            # En iyi bireyi güncelle
            if current_max_fitness > best_fitness:
                best_fitness = current_max_fitness
                best_individual = copy.deepcopy(self.population[fitness_scores.index(current_max_fitness)])
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            self.best_fitness_history.append(best_fitness)

            # Progress raporu
            if generation % 20 == 0 or generation == self.generations - 1:
                avg_fitness = np.mean(fitness_scores)
                print(f"   Nesil {generation}: En iyi={best_fitness:.2f}, Ortalama={avg_fitness:.2f}")

            # Erken durma - stagnation kontrolü
            if stagnation_counter >= max_stagnation:
                print(f"   ⚡ Erken durma: {max_stagnation} nesil iyileşme yok")
                break

            # Yeni nesil oluştur
            new_population = []
            
            # Elitizm - En iyi %10'u koru
            elite_count = max(1, self.population_size // 10)
            elite_indices = sorted(range(len(fitness_scores)), 
                                 key=lambda i: fitness_scores[i], reverse=True)[:elite_count]
            
            for idx in elite_indices:
                new_population.append(copy.deepcopy(self.population[idx]))

            # Kalan popülasyonu crossover ve mutasyon ile oluştur
            while len(new_population) < self.population_size:
                parent1, parent2 = self.selection(fitness_scores)
                child1, child2 = self.crossover(parent1, parent2)
                
                self.mutate(child1)
                self.mutate(child2)
                
                new_population.extend([child1, child2])

            self.population = new_population[:self.population_size]
            return best_individual, best_fitness, self.best_fitness_history