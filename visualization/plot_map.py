import matplotlib.pyplot as plt # type: ignore
from models.drone import Drone
from models.delivery_point import DeliveryPoint
from models.no_fly_zone import NoFlyZone



def plot_map(drones: list[Drone], deliveries: list[DeliveryPoint], no_fly_zones: list[NoFlyZone]):
    fig, ax = plt.subplots()

    for dp in deliveries:
        ax.plot(dp.pos[0], dp.pos[1], 'go' if dp.delivered else 'ro')
        ax.text(dp.pos[0], dp.pos[1], f'{dp.id}', fontsize=9)

    for drone in drones:
        route = [drone.start_pos] + [deliveries[i].pos for i in drone.current_route]
        x = [p[0] for p in route]
        y = [p[1] for p in route]
        ax.plot(x, y, label=f"Drone {drone.id}")
        ax.plot(drone.start_pos[0], drone.start_pos[1], 'bs')  # başlangıç

    for nfz in no_fly_zones:
        polygon = nfz.coordinates + [nfz.coordinates[0]]
        x, y = zip(*polygon)
        ax.plot(x, y, 'k--')
        ax.fill(x, y, color='gray', alpha=0.2)

    ax.set_title("Drone Rotaları ve No-Fly Bölgeleri")
    ax.legend()
    plt.grid(True)
    plt.show()
