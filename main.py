from utils.data_generator import DataGenerator
from algorithms.csp import CSP
from visualization.plot_map import plot_map

def main():
    drones = DataGenerator.generate_drones(3)
    deliveries = DataGenerator.generate_delivery_points(10)
    no_fly_zones = DataGenerator.generate_no_fly_zones(2)

    planner = CSP(drones, deliveries)
    planner.assign_deliveries()

    plot_map(drones, deliveries, no_fly_zones)

if __name__ == "__main__":
    main()
