# main.py - Düzeltilmiş import'lar
from utils import data_generator  # utils.data_generator yerine
from algorithms import csp          # type: ignore # algorithms.csp yerine
from algorithms.a_star import AStar 
from algorithms import genetic  # type: ignore # algorithms.genetic yerine
from visualization import plot_map   # eğer varsa
import time

from algorithms.csp import CSPSolver

def DroneVisualization():
    raise NotImplementedError

def main():
    print("🚁 Drone Filo Optimizasyon Projesi Başlatılıyor...")
    
    # Veri oluşturma
    print("\n📊 Test verisi oluşturuluyor...")
    data_gen = data_generator.DataGenerator()
    drones = data_gen.generate_drones(5)
    deliveries = data_gen.generate_delivery_points(20)
    no_fly_zones = data_gen.generate_no_fly_zones(2)
    
    print(f"✅ {len(drones)} drone, {len(deliveries)} teslimat, {len(no_fly_zones)} yasak bölge oluşturuldu")
    
    # CSP ile temel atama
    print("\n🧩 CSP ile teslimat ataması yapılıyor...")
    start_time = time.time()
    csp_solver = CSPSolver()
    assignments = csp_solver.solve(drones, deliveries, no_fly_zones)
    csp_time = time.time() - start_time
    print(f"⏱️ CSP süresi: {csp_time:.3f} saniye")
    
    # A* ile rota optimizasyonu
    print("\n⭐ A* ile rota optimizasyonu...")
    start_time = time.time()
    astar = AStar(no_fly_zones)
    astar_routes = astar.find_optimal_routes(drones, deliveries, no_fly_zones)
    astar_time = time.time() - start_time
    print(f"⏱️ A* süresi: {astar_time:.3f} saniye")
    
    # Genetic Algorithm ile genel optimizasyon
    print("\n🧬 Genetic Algorithm ile optimizasyon...")
    start_time = time.time()
    ga = genetic.GeneticAlgorithm(population_size=50, mutation_rate=0.1, generations=100)
    best_routes, best_fitness, fitness_history = ga.optimize(drones, deliveries, no_fly_zones)
    ga_time = time.time() - start_time
    print(f"⏱️ GA süresi: {ga_time:.3f} saniye")
    print(f"🎯 En iyi fitness: {best_fitness:.2f}")
    
    # Performans Metrikleri
    print("\n📈 PERFORMANS RAPORİ")
    print("="*50)
    
    total_deliveries = len(deliveries)
    completed_deliveries = sum(len(route) for route in best_routes) if best_routes else 0
    
    completion_rate = (completed_deliveries / total_deliveries) * 100 if total_deliveries > 0 else 0
    total_time = csp_time + astar_time + ga_time
    
    print(f"📦 Toplam teslimat: {total_deliveries}")
    print(f"✅ Tamamlanan teslimat: {completed_deliveries}")
    print(f"📊 Tamamlanma oranı: {completion_rate:.1f}%")
    print(f"⏱️ Toplam algoritma süresi: {total_time:.3f} saniye")
    print(f"🏆 En iyi çözüm fitness: {best_fitness:.2f}")
    
    # Algoritma karşılaştırması
    print(f"\n🔥 ALGORITMA KARŞILAŞTIRMASI")
    print(f"CSP Süresi: {csp_time:.3f}s")
    print(f"A* Süresi: {astar_time:.3f}s") 
    print(f"GA Süresi: {ga_time:.3f}s")
    
    # Görselleştirme
    print("\n🗺️ Sonuçlar görselleştiriliyor...")
    try:
        viz = DroneVisualization()
        viz.plot_routes(drones, deliveries, no_fly_zones, best_routes, 
                       title="Optimized Drone Routes")
        print("✅ Harita başarıyla oluşturuldu!")
    except Exception as e:
        print(f"❌ Görselleştirme hatası: {e}")
    
    print("\n🎉 Proje başarıyla tamamlandı!")
    return {
        'drones': drones,
        'deliveries': deliveries,
        'no_fly_zones': no_fly_zones,
        'best_routes': best_routes,
        'metrics': {
            'completion_rate': completion_rate,
            'total_time': total_time,
            'csp_time': csp_time,
            'astar_time': astar_time,
            'ga_time': ga_time,
            'best_fitness': best_fitness
        }
    }

if __name__ == "__main__":
    results = main()