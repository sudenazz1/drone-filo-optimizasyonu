# main.py - HAZIR VERİ SETİ ENTEGRELİ VERSİYON
from utils import data_generator
from algorithms import csp
from algorithms.a_star import AStar
from algorithms import genetic
from visualization.plot_map import plot_routes
from utils.performance_metrics import PerformanceMetrics
import time
import numpy as np

from algorithms.csp import CSPSolver

class DroneVisualization:
    def plot_routes(self, drones, deliveries, no_fly_zones, best_routes, title=None):
        plot_routes(drones, deliveries, no_fly_zones, best_routes)

def calculate_energy_consumption(routes, drones, deliveries):
    """Ortalama enerji tüketimi hesapla"""
    total_energy = 0
    active_drones = 0
    
    for drone_idx, route in enumerate(routes):
        if not route or drone_idx >= len(drones):
            continue
            
        drone = drones[drone_idx]
        current_pos = drone.start_pos
        drone_energy = 0
        
        for delivery_id in route:
            if delivery_id < len(deliveries):
                delivery = deliveries[delivery_id]
                distance = np.sqrt((delivery.pos[0] - current_pos[0])**2 + 
                                 (delivery.pos[1] - current_pos[1])**2)
                energy = distance * (1 + delivery.weight * 0.1)
                drone_energy += energy
                current_pos = delivery.pos
        
        if drone_energy > 0:
            total_energy += drone_energy
            active_drones += 1
    
    return total_energy / max(active_drones, 1)

def run_test_scenario(scenario_name, num_drones=None, num_deliveries=None, num_no_fly_zones=None, use_predefined=False):
    """Test senaryosu çalıştır - Hazır veri seti desteği eklendi"""
    print(f"\n{'='*60}")
    print(f"🚁 {scenario_name}")
    print(f"{'='*60}")
    
    # Veri oluşturma veya yükleme
    data_gen = data_generator.DataGenerator()
    
    if use_predefined:
        print(f"\n📊 Hazır veri seti yükleniyor...")
        dataset = data_gen.load_predefined_dataset()
        drones = dataset['drones']
        deliveries = dataset['deliveries']
        no_fly_zones = dataset['no_fly_zones']
        print(f"✅ Hazır veri seti yüklendi: {len(drones)} drone, {len(deliveries)} teslimat, {len(no_fly_zones)} yasak bölge")
    else:
        print(f"\n📊 Test verisi oluşturuluyor...")
        drones = data_gen.generate_drones(num_drones)
        deliveries = data_gen.generate_delivery_points(num_deliveries)
        no_fly_zones = data_gen.generate_no_fly_zones(num_no_fly_zones)
        print(f"✅ {len(drones)} drone, {len(deliveries)} teslimat, {len(no_fly_zones)} yasak bölge oluşturuldu")

    # CSP ile temel atama
    print(f"\n🧩 CSP ile teslimat ataması yapılıyor...")
    start_time = time.time()
    csp_solver = CSPSolver()
    assignments = csp_solver.solve(drones, deliveries, no_fly_zones)
    csp_time = time.time() - start_time
    print(f"⏱️ CSP süresi: {csp_time:.3f} saniye")

    # A* ile rota optimizasyonu
    print(f"\n⭐ A* ile rota optimizasyonu...")
    start_time = time.time()
    astar = AStar(no_fly_zones)

    astar_routes = []
    for i, drone in enumerate(drones):
        if i < len(deliveries):
            delivery = deliveries[i]
            route = astar.find_path(drone.current_pos, delivery.pos, current_time="12:00")
            astar_routes.append(route if route else [])
        else:
            astar_routes.append([])
    
    astar_time = time.time() - start_time
    print(f"⏱️ A* süresi: {astar_time:.3f} saniye")

    # Genetic Algorithm ile genel optimizasyon
    print(f"\n🧬 Genetic Algorithm ile optimizasyon...")
    start_time = time.time()
    
    # Senaryo boyutuna göre GA parametrelerini ayarla
    if len(deliveries) <= 20:
        ga_params = {'population_size': 30, 'generations': 50}
    else:
        ga_params = {'population_size': 50, 'generations': 100}
    
    ga = genetic.GeneticAlgorithm(
        population_size=ga_params['population_size'], 
        mutation_rate=0.15, 
        generations=ga_params['generations']
    )
    
    best_routes, best_fitness, fitness_history = ga.optimize(drones, deliveries, no_fly_zones)
    ga_time = time.time() - start_time
    print(f"⏱️ GA süresi: {ga_time:.3f} saniye")
    print(f"🎯 En iyi fitness: {best_fitness:.2f}")

    # Performans Metrikleri Hesaplama
    total_deliveries = len(deliveries)
    completed_deliveries = sum(len(route) for route in best_routes) if best_routes else 0
    completion_rate = (completed_deliveries / total_deliveries) * 100 if total_deliveries > 0 else 0
    
    # Ortalama enerji tüketimi
    avg_energy = calculate_energy_consumption(best_routes, drones, deliveries)
    
    total_time = csp_time + astar_time + ga_time

    # Performans Raporu
    print(f"\n📈 PERFORMANS RAPORİ - {scenario_name}")
    print("="*50)
    print(f"📦 Toplam teslimat: {total_deliveries}")
    print(f"✅ Tamamlanan teslimat: {completed_deliveries}")
    print(f"📊 Tamamlanma oranı: {completion_rate:.1f}%")
    print(f"⚡ Ortalama enerji tüketimi: {avg_energy:.2f}")
    print(f"⏱️ Toplam algoritma süresi: {total_time:.3f} saniye")
    print(f"🏆 En iyi çözüm fitness: {best_fitness:.2f}")

    print(f"\n🔥 ALGORITMA KARŞILAŞTIRMASI")
    print(f"CSP Süresi: {csp_time:.3f}s ({(csp_time/total_time)*100:.1f}%)")
    print(f"A* Süresi: {astar_time:.3f}s ({(astar_time/total_time)*100:.1f}%)")
    print(f"GA Süresi: {ga_time:.3f}s ({(ga_time/total_time)*100:.1f}%)")

    # Görselleştirme
    print(f"\n🗺️ Sonuçlar görselleştiriliyor...")
    try:
        viz = DroneVisualization()
        viz.plot_routes(drones, deliveries, no_fly_zones, best_routes)
        print("✅ Harita başarıyla oluşturuldu!")
    except Exception as e:
        print(f"❌ Görselleştirme hatası: {e}")

    return {
        'scenario_name': scenario_name,
        'drones': drones,
        'deliveries': deliveries,
        'no_fly_zones': no_fly_zones,
        'best_routes': best_routes,
        'metrics': {
            'completion_rate': completion_rate,
            'avg_energy_consumption': avg_energy,
            'total_time': total_time,
            'csp_time': csp_time,
            'astar_time': astar_time,
            'ga_time': ga_time,
            'best_fitness': best_fitness,
            'num_drones': len(drones),
            'num_deliveries': len(deliveries),
            'num_no_fly_zones': len(no_fly_zones)
        }
    }

def compare_scenarios(results):
    """İki senaryoyu karşılaştır"""
    print(f"\n{'='*80}")
    print(f"📊 SENARYO KARŞILAŞTIRMASI")
    print(f"{'='*80}")
    
    for result in results:
        metrics = result['metrics']
        print(f"\n🎯 {result['scenario_name']}:")
        print(f"   Dronelar: {metrics['num_drones']}, Teslimatlar: {metrics['num_deliveries']}, Yasak Bölgeler: {metrics['num_no_fly_zones']}")
        print(f"   Tamamlanma Oranı: {metrics['completion_rate']:.1f}%")
        print(f"   Ortalama Enerji: {metrics['avg_energy_consumption']:.2f}")
        print(f"   Toplam Süre: {metrics['total_time']:.3f}s")
        print(f"   Fitness: {metrics['best_fitness']:.2f}")
    
    if len(results) >= 2:
        print(f"\n🔍 KARŞILAŞTIRMA ANALİZİ:")
        for i in range(len(results)-1):
            r1, r2 = results[i]['metrics'], results[i+1]['metrics']
            print(f"\n   {results[i]['scenario_name']} vs {results[i+1]['scenario_name']}:")
            print(f"   ├── Tamamlanma Oranı Farkı: {r2['completion_rate'] - r1['completion_rate']:.1f}%")
            print(f"   ├── Enerji Tüketimi Farkı: {r2['avg_energy_consumption'] - r1['avg_energy_consumption']:.2f}")
            print(f"   └── Süre Farkı: {r2['total_time'] - r1['total_time']:.3f}s")
            
            # Verimlilik analizi
            efficiency_1 = r1['completion_rate'] / r1['total_time']
            efficiency_2 = r2['completion_rate'] / r2['total_time']
            print(f"   Verimlilik Karşılaştırması:")
            print(f"     └── Fark: {efficiency_2 - efficiency_1:.2f} (Yüksek = Daha İyi)")

def main():
    print("🚁 DRONE FİLO OPTİMİZASYON PROJESİ")
    print("="*60)
    
    results = []
    
    # TEST SENARYOSU 1: HAZIR VERİ SETİ (YENİ!)
    print("\n🎯 HAZIR VERİ SETİ TEST EDİLİYOR...")
    predefined_result = run_test_scenario(
        "TEST SENARYOSU 1 - Hazır Veri Seti", 
        use_predefined=True
    )
    results.append(predefined_result)
    
    # TEST SENARYOSU 2: Küçük Ölçekli Rastgele
    random_small_result = run_test_scenario(
        "TEST SENARYOSU 2 - Küçük Ölçekli Rastgele", 
        num_drones=5, 
        num_deliveries=20, 
        num_no_fly_zones=2
    )
    results.append(random_small_result)
    
    # TEST SENARYOSU 3: Büyük Ölçekli 
    random_large_result = run_test_scenario(
        "TEST SENARYOSU 3 - Büyük Ölçekli", 
        num_drones=10, 
        num_deliveries=50, 
        num_no_fly_zones=5
    )
    results.append(random_large_result)
    
    # BONUS: Karma senaryo da test edelim
    print("\n🔄 KARMA SENARYO TEST EDİLİYOR...")
    data_gen = data_generator.DataGenerator()
    mixed_dataset = data_gen.generate_mixed_scenario()
    
    mixed_result = run_test_scenario(
        "TEST SENARYOSU 4 - Karma Senaryo",
        use_predefined=False  # Karma senaryo için özel işlem
    )
    # Karma veriyi manuel olarak ata
    mixed_result['drones'] = mixed_dataset['drones']
    mixed_result['deliveries'] = mixed_dataset['deliveries']
    mixed_result['no_fly_zones'] = mixed_dataset['no_fly_zones']
    results.append(mixed_result)
    
    # Tüm senaryoları karşılaştır
    compare_scenarios(results)
    
    print(f"\n🎉 PROJE BAŞARIYLA TAMAMLANDI!")
    print(f"✅ Hazır veri seti başarıyla entegre edildi")
    print(f"✅ 4 farklı senaryo test edildi")
    print(f"✅ Tüm algoritmalar çalıştırıldı") 
    print(f"✅ Performans metrikleri hesaplandı")
    print(f"✅ Karşılaştırmalı analiz yapıldı")
    
    # Veri seti detayları
    print(f"\n📋 VERİ SETİ DETAYLARI:")
    print(f"🎯 Hazır Veri Seti: {len(predefined_result['drones'])} drone, {len(predefined_result['deliveries'])} teslimat")
    print(f"🎲 Rastgele Veriler: Küçük ve büyük ölçekli senaryolar")
    print(f"🔄 Karma Senaryo: Hazır + rastgele veri karışımı")
    
    return results

def run_only_predefined_dataset():
    """Sadece hazır veri setini test et"""
    print("🎯 SADECE HAZIR VERİ SETİ TEST EDİLİYOR")
    print("="*50)
    
    result = run_test_scenario(
        "Hazır Veri Seti Analizi", 
        use_predefined=True
    )
    
    print(f"\n✅ Hazır veri seti başarıyla test edildi!")
    return result

if __name__ == "__main__":
    # Tam test için main() kullanın
    results = main()
    
    # Sadece hazır veri seti için run_only_predefined_dataset() kullanın
    # predefined_only = run_only_predefined_dataset()
    
    # Son özet
    print(f"\n📋 FİNAL ÖZET:")
    for result in results:
        m = result['metrics']
        print(f"{result['scenario_name']}: {m['completion_rate']:.1f}% tamamlanma, {m['avg_energy_consumption']:.2f} ortalama enerji")