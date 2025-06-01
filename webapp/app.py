import sys
import os
# Ana proje klasörünü Python path'ine ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request
from utils.data_generator import DataGenerator
from algorithms.csp import CSP
from algorithms.a_star import AStar
from algorithms.genetic import GeneticAlgorithm

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate_scenario', methods=['POST'])
def generate_scenario():
    try:
        data = request.get_json()
        num_drones = data.get('drones', 5)
        num_deliveries = data.get('deliveries', 20)
        num_no_fly_zones = data.get('no_fly_zones', 2)
        
        drones = DataGenerator.generate_drones(num_drones)
        deliveries = DataGenerator.generate_delivery_points(num_deliveries)
        no_fly_zones = DataGenerator.generate_no_fly_zones(num_no_fly_zones)
        
        return jsonify({
            'success': True,
            'drones': [{'id': d.id, 'pos': d.start_pos, 'battery': d.battery} for d in drones],
            'deliveries': [{'id': d.id, 'pos': d.pos, 'priority': d.priority} for d in deliveries],
            'no_fly_zones': [{'id': nfz.id, 'coordinates': nfz.coordinates} for nfz in no_fly_zones]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/optimize', methods=['POST'])
def optimize_routes():
    try:
        data = request.get_json()
        # Optimizasyon kodunu buraya ekleyin
        return jsonify({
            'success': True,
            'message': 'Optimizasyon tamamlandı'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🌐 Web server başlatılıyor...")
    print("📍 http://localhost:5000 adresinde erişilebilir")
    app.run(debug=True, port=5000)