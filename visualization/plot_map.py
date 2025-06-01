import matplotlib.pyplot as plt # type: ignore
from models.drone import Drone
from models.delivery_point import DeliveryPoint
from models.no_fly_zone import NoFlyZone
from typing import List

def plot_routes(drones: List[Drone], deliveries: List[DeliveryPoint], 
                no_fly_zones: List[NoFlyZone], best_routes: List[List[int]], 
                title: str = "Drone Rotaları ve No-Fly Bölgeleri"):
    """İyileştirilmiş görselleştirme - title parametresi eklendi"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Sol grafik: Rotalar ve harita
    # No-fly zones çizimi (zaman bilgisi ile)
    for nfz in no_fly_zones:
        polygon = nfz.coordinates + [nfz.coordinates[0]]
        x, y = zip(*polygon)
        ax1.plot(x, y, 'k--', linewidth=2)
        ax1.fill(x, y, color='red', alpha=0.3)
        # Zaman bilgisini ekle
        center_x = sum(coord[0] for coord in nfz.coordinates) / len(nfz.coordinates)
        center_y = sum(coord[1] for coord in nfz.coordinates) / len(nfz.coordinates)
        ax1.text(center_x, center_y, f'NFZ{nfz.id}\n{nfz.active_time[0]}-{nfz.active_time[1]}', 
                ha='center', va='center', fontsize=8, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

    # Teslimat noktaları (önceliğe göre renklendirme)
    for dp in deliveries:
        if dp.priority >= 4:  # Acil teslimat
            color = 'orange' if dp.delivered else 'red'
            marker = 's'  # Kare
        else:
            color = 'lightgreen' if dp.delivered else 'lightcoral'
            marker = 'o'  # Daire
        
        ax1.plot(dp.pos[0], dp.pos[1], color=color, marker=marker, markersize=8)
        ax1.text(dp.pos[0], dp.pos[1], f'{dp.id}\nP{dp.priority}', 
                fontsize=7, ha='center', va='bottom')

    # Drone rotaları ve başlangıç noktaları
    colors = ['blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta']
    for i, route in enumerate(best_routes):
        if i >= len(drones) or not route:
            continue
            
        color = colors[i % len(colors)]
        route_points = [drones[i].start_pos] + [deliveries[idx].pos for idx in route if idx < len(deliveries)]
        
        if len(route_points) > 1:
            x = [p[0] for p in route_points]
            y = [p[1] for p in route_points]
            ax1.plot(x, y, color=color, marker='o', linewidth=2, 
                    label=f'Drone {drones[i].id} ({len(route)} teslimat)')

        # Drone başlangıç noktası - büyük kare ile işaretle
        ax1.plot(drones[i].start_pos[0], drones[i].start_pos[1], 
                color=color, marker='s', markersize=12, markeredgecolor='black', markeredgewidth=2)
        ax1.text(drones[i].start_pos[0], drones[i].start_pos[1], f'D{drones[i].id}', 
                ha='center', va='center', fontweight='bold', color='white')

    ax1.set_title(title)
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('X Koordinatı')
    ax1.set_ylabel('Y Koordinatı')
    
    # Sağ grafik: Performans metrikleri
    from utils.performance_metrics import PerformanceMetrics
    metrics = PerformanceMetrics.calculate_efficiency_metrics(drones, deliveries)
    
    # Bar chart
    metric_names = ['Tamamlanma\nOranı (%)', 'Ortalama Enerji\nTüketimi', 'Enerji\nVerimliliği', 'İhlal\nOranı']
    metric_values = [
        metrics['completion_rate'],
        metrics['average_energy_consumption'] / 100,  # Ölçeklendirme
        metrics['energy_efficiency_ratio'] * 100,
        metrics['violation_rate'] * 100
    ]
    
    bars = ax2.bar(metric_names, metric_values, color=['green', 'blue', 'orange', 'red'], alpha=0.7)
    ax2.set_title('Performans Metrikleri')
    ax2.set_ylabel('Değer')
    
    # Bar değerlerini yazdır
    for bar, value in zip(bars, metric_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()