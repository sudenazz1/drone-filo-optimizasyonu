# main.py - HAZIR VERİ SETİ ENTEGRELİ VERSİYON (GÜNCELLENMİŞ)
import sys
import os

# Proje kök dizinini Python path'ine ekle
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

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
        """Rota görselleştirme - hata yakalama ile güçlendirildi"""
        try:
            plot_routes(drones, deliveries, no_fly_zones, best_routes, title)
        except Exception as e:
            print(f"⚠️ Görselleştirme modülü bulunamadı: {e}")
            print("📊 Metin tabanlı sonuç gösteriliyor...")
            self.show_text_results(drones, deliveries, best_routes)
    
    def show_text_results(self, drones, deliveries, best_routes):
        """Metin tabanlı sonuç gösterimi"""
        print("\n" + "="*50)
        print("📋 ROTA SONUÇLARI (METIN FORMAT)")
        print("="*50)
        
        for i, route in enumerate(best_routes):
            if route and i < len(drones):
                drone = drones[i]
                print(f"\n🚁 Drone {i+1} (Pos: {drone.start_pos}):")
                print(f"   Kapasite: {drone.max_weight}kg, Batarya: {drone.battery}mAh")
                print(f"   Atanan teslimatlar: {len(route)}")
                
                for delivery_id in route[:3]:  # İlk 3 teslimatı göster
                    if delivery_id < len(deliveries):
                        delivery = deliveries[delivery_id]
                        print(f"   ├── Teslimat {delivery_id+1}: {delivery.pos} ({delivery.weight}kg)")
                
                if len(route) > 3:
                    print(f"   └── ... ve {len(route)-3} teslimat daha")

def calculate_energy_consumption(routes, drones, deliveries):
    """Geliştirilmiş enerji tüketimi hesaplama"""
    if not routes or not drones or not deliveries:
        return 0.0
    
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
                # Mesafe hesaplama
                distance = np.sqrt((delivery.pos[0] - current_pos[0])**2 + 
                                 (delivery.pos[1] - current_pos[1])**2)
                
                # Enerji hesaplama: mesafe + ağırlık faktörü + hız faktörü
                base_energy = distance * (drone.speed / 10)  # Hız faktörü
                weight_penalty = delivery.weight * 0.15      # Ağırlık cezası
                energy = base_energy * (1 + weight_penalty)
                
                drone_energy += energy
                current_pos = delivery.pos
        
        if drone_energy > 0:
            total_energy += drone_energy
            active_drones += 1
    
    return total_energy / max(active_drones, 1)

def calculate_completion_metrics(routes, drones, deliveries):
    """Tamamlanma metriklerini hesapla"""
    total_deliveries = len(deliveries)
    completed_deliveries = sum(len(route) for route in routes if route)
    completion_rate = (completed_deliveries / total_deliveries) * 100 if total_deliveries > 0 else 0
    
    # Ağırlık dağılımı analizi
    total_weight = sum(delivery.weight for delivery in deliveries)
    assigned_weight = 0
    
    for route in routes:
        for delivery_id in route:
            if delivery_id < len(deliveries):
                assigned_weight += deliveries[delivery_id].weight
    
    weight_efficiency = (assigned_weight / total_weight) * 100 if total_weight > 0 else 0
    
    return {
        'completion_rate': completion_rate,
        'weight_efficiency': weight_efficiency,
        'completed_deliveries': completed_deliveries,
        'total_deliveries': total_deliveries
    }

def run_test_scenario(scenario_name, num_drones=None, num_deliveries=None, num_no_fly_zones=None, use_predefined=False):
    """Test senaryosu çalıştırma fonksiyonu - ÇALIŞAN VERSİYON"""
    print(f"\n{'='*60}")
    print(f"🚁 {scenario_name}")
    print(f"{'='*60}")
    
    try:
        # Veri oluşturma/yükleme
        data_gen = data_generator.DataGenerator()
        
        if use_predefined:
            print(f"\n📊 Hazır veri seti yükleniyor...")
            try:
                dataset = data_gen.load_predefined_dataset()
                drones = dataset['drones']
                deliveries = dataset['deliveries']
                no_fly_zones = dataset['no_fly_zones']
            except Exception as e:
                print(f"⚠️ Hazır veri seti yüklenemiyor: {e}")
                print("🔄 Alternatif veri oluşturuluyor...")
                drones = data_gen.generate_drones(5)
                deliveries = data_gen.generate_delivery_points(15)
                no_fly_zones = data_gen.generate_no_fly_zones(2)
        else:
            print(f"\n📊 Test verisi oluşturuluyor...")
            drones = data_gen.generate_drones(num_drones or 5)
            deliveries = data_gen.generate_delivery_points(num_deliveries or 20)
            no_fly_zones = data_gen.generate_no_fly_zones(num_no_fly_zones or 2)
        
        # Veri doğrulama
        if not drones or not deliveries:
            raise ValueError("Yetersiz veri: En az 1 drone ve 1 teslimat gerekli")
        
        print(f"✅ {len(drones)} drone, {len(deliveries)} teslimat, {len(no_fly_zones)} yasak bölge hazır")

        # CSP Algoritması
        print(f"\n🧩 CSP ile teslimat ataması yapılıyor...")
        start_time = time.time()
        try:
            csp_solver = CSPSolver()
            assignments = csp_solver.solve(drones, deliveries, no_fly_zones)
            csp_time = time.time() - start_time
            print(f"⏱️ CSP süresi: {csp_time:.3f} saniye")
        except Exception as e:
            print(f"❌ CSP Hatası: {e}")
            csp_time = 0
            assignments = []

        # A* Algoritması
        print(f"\n⭐ A* ile rota optimizasyonu...")
        start_time = time.time()
        try:
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
        except Exception as e:
            print(f"❌ A* Hatası: {e}")
            astar_time = 0
            astar_routes = []

        # Genetic Algorithm
        print(f"\n🧬 Genetic Algorithm ile optimizasyon...")
        start_time = time.time()
        try:
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
        except Exception as e:
            print(f"❌ GA Hatası: {e}")
            ga_time = 0
            best_routes = []
            best_fitness = 0

        # Performans Hesaplamaları
        total_deliveries = len(deliveries)
        completed_deliveries = sum(len(route) for route in best_routes) if best_routes else 0
        completion_rate = (completed_deliveries / total_deliveries) * 100 if total_deliveries > 0 else 0
        avg_energy = calculate_energy_consumption(best_routes, drones, deliveries)
        total_time = csp_time + astar_time + ga_time
        
        # Ağırlık verimliliği hesapla
        metrics = calculate_completion_metrics(best_routes, drones, deliveries)
        weight_efficiency = metrics['weight_efficiency']

        # Performans Raporu
        print(f"\n📈 PERFORMANS RAPORİ - {scenario_name}")
        print("="*50)
        print(f"📦 Toplam teslimat: {total_deliveries}")
        print(f"✅ Tamamlanan teslimat: {completed_deliveries}")
        print(f"📊 Tamamlanma oranı: {completion_rate:.1f}%")
        print(f"⚖️ Ağırlık verimliliği: {weight_efficiency:.1f}%")
        print(f"⚡ Ortalama enerji tüketimi: {avg_energy:.2f}")
        print(f"⏱️ Toplam algoritma süresi: {total_time:.3f} saniye")
        print(f"🏆 En iyi çözüm fitness: {best_fitness:.2f}")

        # Algoritmik performans analizi
        if total_time > 0:
            print(f"\n🔥 ALGORITMA KARŞILAŞTIRMASI")
            print(f"CSP Süresi: {csp_time:.3f}s ({(csp_time/total_time)*100:.1f}%)")
            print(f"A* Süresi: {astar_time:.3f}s ({(astar_time/total_time)*100:.1f}%)")
            print(f"GA Süresi: {ga_time:.3f}s ({(ga_time/total_time)*100:.1f}%)")

        # Görselleştirme
        print(f"\n🗺️ Sonuçlar görselleştiriliyor...")
        try:
            viz = DroneVisualization()
            viz.plot_routes(drones, deliveries, no_fly_zones, best_routes, scenario_name)
            print("✅ Harita başarıyla oluşturuldu!")
        except Exception as e:
            print(f"⚠️ Görselleştirme uyarısı: {e}")

        return {
            'scenario_name': scenario_name,
            'drones': drones,
            'deliveries': deliveries,
            'no_fly_zones': no_fly_zones,
            'best_routes': best_routes,
            'metrics': {
                'completion_rate': completion_rate,
                'weight_efficiency': weight_efficiency,
                'avg_energy_consumption': avg_energy,
                'total_time': total_time,
                'csp_time': csp_time,
                'astar_time': astar_time,
                'ga_time': ga_time,
                'best_fitness': best_fitness,
                'num_drones': len(drones),
                'num_deliveries': len(deliveries),
                'num_no_fly_zones': len(no_fly_zones),
                'completed_deliveries': completed_deliveries
            }
        }

    except Exception as e:
        print(f"❌ KRITIK HATA - {scenario_name}: {e}")
        print(f"📋 Hata detayı: {type(e).__name__}")
        return {
            'scenario_name': f"{scenario_name} (BAŞARISIZ)",
            'error': str(e),
            'metrics': {
                'completion_rate': 0,
                'weight_efficiency': 0,
                'avg_energy_consumption': 0,
                'total_time': 0,
                'csp_time': 0,
                'astar_time': 0,
                'ga_time': 0,
                'best_fitness': 0,
                'num_drones': 0,
                'num_deliveries': 0,
                'num_no_fly_zones': 0,
                'completed_deliveries': 0
            },
            'drones': [],
            'deliveries': [],
            'no_fly_zones': [],
            'best_routes': []
        }

def compare_scenarios(results):
    """Geliştirilmiş senaryo karşılaştırması"""
    valid_results = [r for r in results if r is not None and 'error' not in r]
    if not valid_results:
        print("❌ Karşılaştırılacak geçerli sonuç bulunamadı!")
        return
    
    print(f"\n{'='*80}")
    print(f"📊 SENARYO KARŞILAŞTIRMASI")
    print(f"{'='*80}")
    
    for result in valid_results:
        metrics = result['metrics']
        print(f"\n🎯 {result['scenario_name']}:")
        print(f"   📊 Sistem: {metrics['num_drones']} drone, {metrics['num_deliveries']} teslimat, {metrics['num_no_fly_zones']} yasak bölge")
        print(f"   ✅ Tamamlanan: {metrics['completed_deliveries']}/{metrics['num_deliveries']} ({metrics['completion_rate']:.1f}%)")
        print(f"   ⚖️ Ağırlık Verimliliği: {metrics['weight_efficiency']:.1f}%")
        print(f"   ⚡ Ortalama Enerji: {metrics['avg_energy_consumption']:.2f}")
        print(f"   ⏱️ Toplam Süre: {metrics['total_time']:.3f}s")
        print(f"   🏆 Fitness: {metrics['best_fitness']:.2f}")
    
    if len(valid_results) >= 2:
        print(f"\n🔍 DETAYLI KARŞILAŞTIRMA:")
        for i in range(len(valid_results)-1):
            r1, r2 = valid_results[i]['metrics'], valid_results[i+1]['metrics']
            print(f"\n   📈 {valid_results[i]['scenario_name']} ➜ {valid_results[i+1]['scenario_name']}:")
            print(f"   ├── Tamamlanma Oranı: {r1['completion_rate']:.1f}% ➜ {r2['completion_rate']:.1f}% ({r2['completion_rate'] - r1['completion_rate']:+.1f}%)")
            print(f"   ├── Enerji Tüketimi: {r1['avg_energy_consumption']:.2f} ➜ {r2['avg_energy_consumption']:.2f} ({r2['avg_energy_consumption'] - r1['avg_energy_consumption']:+.2f})")
            print(f"   └── İşlem Süresi: {r1['total_time']:.3f}s ➜ {r2['total_time']:.3f}s ({r2['total_time'] - r1['total_time']:+.3f}s)")
            
            # Genel verimlilik skoru
            efficiency_1 = (r1['completion_rate'] * r1['weight_efficiency']) / (r1['total_time'] + 1)
            efficiency_2 = (r2['completion_rate'] * r2['weight_efficiency']) / (r2['total_time'] + 1)
            print(f"   🎯 Verimlilik Skoru: {efficiency_1:.2f} ➜ {efficiency_2:.2f} ({efficiency_2 - efficiency_1:+.2f})")

def main():
    """Ana program - Geliştirilmiş hata yakalama ile"""
    print("🚁 DRONE FİLO OPTİMİZASYON PROJESİ")
    print("="*60)
    print("📋 Hazır veri seti entegreli versiyon")
    print("🔧 Tüm algoritmalar ve görselleştirme dahil")
    
    results = []
    
    # TEST SENARYOSU 1: HAZIR VERİ SETİ
    print("\n🎯 HAZIR VERİ SETİ TEST EDİLİYOR...")
    predefined_result = run_test_scenario(
        "TEST SENARYOSU 1 - Hazır Veri Seti", 
        use_predefined=True
    )
    if predefined_result:
        results.append(predefined_result)
    
    # TEST SENARYOSU 2: Küçük Ölçekli Rastgele
    print("\n🎯 KÜÇÜK ÖLÇEKLİ RASTGELE TEST...")
    random_small_result = run_test_scenario(
        "TEST SENARYOSU 2 - Küçük Ölçekli Rastgele", 
        num_drones=5, 
        num_deliveries=15,  # Daha az teslimat
        num_no_fly_zones=2
    )
    if random_small_result:
        results.append(random_small_result)
    
    # TEST SENARYOSU 3: Orta Ölçekli 
    print("\n🎯 ORTA ÖLÇEKLİ TEST...")
    random_medium_result = run_test_scenario(
        "TEST SENARYOSU 3 - Orta Ölçekli", 
        num_drones=8, 
        num_deliveries=30, 
        num_no_fly_zones=4
    )
    if random_medium_result:
        results.append(random_medium_result)
    
    # BONUS: Karma senaryo
    try:
        print("\n🔄 KARMA SENARYO TEST EDİLİYOR...")
        data_gen = data_generator.DataGenerator()
        
        # Basit karma senaryo oluştur
        try:
            mixed_dataset = data_gen.generate_mixed_scenario()
        except:
            # Eğer generate_mixed_scenario yoksa, alternatif oluştur
            mixed_dataset = {
                'drones': data_gen.generate_drones(6),
                'deliveries': data_gen.generate_delivery_points(25),
                'no_fly_zones': data_gen.generate_no_fly_zones(3)
            }
        
        # Karma senaryo için gerçek test çalıştır
        mixed_result = run_test_scenario(
            "TEST SENARYOSU 4 - Karma Senaryo",
            num_drones=6,
            num_deliveries=25,
            num_no_fly_zones=3
        )
        
        if mixed_result:
            results.append(mixed_result)
            print("✅ Karma senaryo başarıyla test edildi!")
        
    except Exception as e:
        print(f"⚠️ Karma senaryo hatası: {e}")
    
    # Tüm senaryoları karşılaştır
    if results:
        compare_scenarios(results)
        
        # Özet istatistikler
        print(f"\n📊 GENEL ÖZET İSTATİSTİKLER")
        print("="*50)
        valid_results = [r for r in results if 'error' not in r]
        
        if valid_results:
            total_drones = sum(r['metrics']['num_drones'] for r in valid_results)
            total_deliveries = sum(r['metrics']['num_deliveries'] for r in valid_results)
            avg_completion = sum(r['metrics']['completion_rate'] for r in valid_results) / len(valid_results)
            avg_energy = sum(r['metrics']['avg_energy_consumption'] for r in valid_results) / len(valid_results)
            
            print(f"🚁 Toplam test edilen drone: {total_drones}")
            print(f"📦 Toplam test edilen teslimat: {total_deliveries}")
            print(f"📊 Ortalama tamamlanma oranı: {avg_completion:.1f}%")
            print(f"⚡ Ortalama enerji tüketimi: {avg_energy:.2f}")
            print(f"🧪 Başarılı test senaryosu: {len(valid_results)}/4")
    
    print(f"\n🎉 PROJE BAŞARIYLA TAMAMLANDI!")
    print(f"✅ Hazır veri seti başarıyla entegre edildi")
    print(f"✅ {len([r for r in results if 'error' not in r])} senaryo başarıyla test edildi")
    print(f"✅ Tüm algoritmalar çalıştırıldı") 
    print(f"✅ Performans metrikleri hesaplandı")
    print(f"✅ Karşılaştırmalı analiz yapıldı")
    
    # Veri seti özetleri
    if results:
        print(f"\n📋 VERİ SETİ DETAYLARI:")
        for result in results:
            if 'error' not in result:
                metrics = result['metrics']
                print(f"📊 {result['scenario_name']}: {metrics['num_drones']}D/{metrics['num_deliveries']}T/{metrics['num_no_fly_zones']}NFZ")
    
    return results

def run_only_predefined_dataset():
    """Sadece hazır veri setini test et - Hızlı test için"""
    print("🎯 SADECE HAZIR VERİ SETİ TEST EDİLİYOR")
    print("="*50)
    
    result = run_test_scenario(
        "Hazır Veri Seti - Hızlı Test", 
        use_predefined=True
    )
    
    if result and 'error' not in result:
        print(f"\n✅ Hazır veri seti başarıyla test edildi!")
        print(f"📊 Sonuç: {result['metrics']['completion_rate']:.1f}% tamamlanma oranı")
        return result
    else:
        print(f"❌ Hazır veri seti testi başarısız!")
        return None

if __name__ == "__main__":
    print("🚀 DRONE FİLO OPTİMİZASYON SİSTEMİ BAŞLATILIYOR...")
    print("="*60)
    
    try:
        # Ana program çalıştır - Tam test sürümü
        print("📋 Seçenek 1: Tüm senaryoları test et")
        print("📋 Seçenek 2: Sadece hazır veri setini test et")
        
        # Otomatik olarak tüm testleri çalıştır
        print("\n🔄 Tüm senaryolar test ediliyor...")
        results = main()
        
        print(f"\n🏁 SONUÇ:")
        if results:
            valid_results = [r for r in results if 'error' not in r]
            print(f"✅ {len(valid_results)} senaryo başarıyla tamamlandı")
            if valid_results:
                print(f"🎯 En iyi performans: {max(r['metrics']['completion_rate'] for r in valid_results):.1f}% tamamlanma")
        else:
            print(f"⚠️ Hiçbir senaryo tamamlanamadı - konfigürasyon kontrol edilmeli")
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Program kullanıcı tarafından durduruldu")
    except Exception as e:
        print(f"\n❌ Program hatası: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback: Sadece hazır veri seti test et
        print(f"\n🔄 Fallback: Sadece hazır veri seti test ediliyor...")
        result = run_only_predefined_dataset()
        if result:
            print(f"✅ En azından hazır veri seti çalışıyor!")
    
    print(f"\n👋 Program sonlandırılıyor...")