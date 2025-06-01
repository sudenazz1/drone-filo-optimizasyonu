import matplotlib.pyplot as plt # type: ignore
from models.drone import Drone
from models.delivery_point import DeliveryPoint
from models.no_fly_zone import NoFlyZone

def plot_routes(drones: list[Drone], deliveries: list[DeliveryPoint], no_fly_zones: list[NoFlyZone], best_routes: list[list[int]]):
    fig, ax = plt.subplots()

    # No-fly zones çizimi
    for nfz in no_fly_zones:
        polygon = nfz.coordinates + [nfz.coordinates[0]]
        x, y = zip(*polygon)
        ax.plot(x, y, 'k--')
        ax.fill(x, y, color='gray', alpha=0.2)

    # Teslimat noktaları
    for dp in deliveries:
        ax.plot(dp.pos[0], dp.pos[1], 'go' if dp.delivered else 'ro')
        ax.text(dp.pos[0], dp.pos[1], f'{dp.id}', fontsize=9)

    # Drone rotaları ve başlangıç noktaları
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for i, route in enumerate(best_routes):
        color = colors[i % len(colors)]
        if len(route) == 0:
            continue
        route_points = [drones[i].start_pos] + [deliveries[idx].pos for idx in route]
        x = [p[0] for p in route_points]
        y = [p[1] for p in route_points]
        ax.plot(x, y, color=color, marker='o', label=f'Drone {drones[i].id} Rotası')

        # Drone başlangıç noktası kare ile işaretle
        ax.plot(drones[i].start_pos[0], drones[i].start_pos[1], color + 's')

    ax.set_title("Drone Rotaları ve No-Fly Bölgeleri")
    ax.legend()
    plt.grid(True)
    plt.show()
