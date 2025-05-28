from utils.data_generator import DataGenerator
from algorithms.csp import CSP
from algorithms.genetic import GeneticAlgorithm

def test_csp():
    drones = DataGenerator.generate_drones(3)
    deliveries = DataGenerator.generate_delivery_points(10)
    planner = CSP(drones, deliveries)
    planner.assign_deliveries()

    print("CSP Sonuçları:")
    for d in deliveries:
        print(f"Teslimat {d.id}: Drone {d.assigned_to}, Teslimat zamanı: {d.delivery_time}")

def test_genetic():
    deliveries = DataGenerator.generate_delivery_points(10)
    ga = GeneticAlgorithm(deliveries)
    best_sequence = ga.run()

    print("Genetik Algoritma Sıralaması (teslimat ID'leri):")
    print(best_sequence)

if __name__ == "__main__":
    print("--- CSP Testi ---")
    test_csp()
    print("\n--- Genetik Algoritma Testi ---")
    test_genetic()

