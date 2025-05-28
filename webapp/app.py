from flask import Flask, render_template, jsonify
from utils.data_generator import DataGenerator
from algorithms.csp import CSP
from models.drone import Drone
from models.delivery_point import DeliveryPoint
from models.no_fly_zone import NoFlyZone

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run")
def run_simulation():
    drones = DataGenerator.generate_drones(3)
    deliveries = DataGenerator.generate_delivery_points(10)
    no_fly_zones = DataGenerator.generate_no_fly_zones(2)

    planner = CSP(drones, deliveries)
    planner.assign_deliveries()

    results = {
        "drones": [
            {
                "id": d.id,
                "route": [dp for dp in d.current_route],
                "energy": d.energy_consumed,
                "distance": d.total_distance
            } for d in drones
        ],
        "deliveries": [
            {
                "id": dp.id,
                "assigned_to": dp.assigned_to,
                "delivered": dp.delivered,
                "pos": dp.pos,
                "priority": dp.priority
            } for dp in deliveries
        ]
    }

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
