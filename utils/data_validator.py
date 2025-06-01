# utils/data_validator.py
from typing import List
from models.drone import Drone
from models.delivery_point import DeliveryPoint
from models.no_fly_zone import NoFlyZone

class DataValidator:
    """Veri doğrulama sınıfı - Eksik olan güvenlik katmanı"""
    
    @staticmethod
    def validate_drones(drones: List[Drone]) -> tuple[bool, List[str]]:
        """Drone verilerini doğrula"""
        errors = []
        
        if not drones:
            errors.append("❌ En az 1 drone gerekli")
            return False, errors
        
        for drone in drones:
            if drone.max_weight <= 0:
                errors.append(f"❌ Drone {drone.id}: Geçersiz maksimum ağırlık ({drone.max_weight})")
            
            if drone.battery <= 0:
                errors.append(f"❌ Drone {drone.id}: Geçersiz batarya seviyesi ({drone.battery})")
            
            if drone.speed <= 0:
                errors.append(f"❌ Drone {drone.id}: Geçersiz hız ({drone.speed})")
            
            # Pozisyon kontrolü
            x, y = drone.start_pos
            if not (0 <= x <= 100) or not (0 <= y <= 100):
                errors.append(f"❌ Drone {drone.id}: Geçersiz başlangıç pozisyonu ({x}, {y})")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_deliveries(deliveries: List[DeliveryPoint]) -> tuple[bool, List[str]]:
        """Teslimat verilerini doğrula"""
        errors = []
        
        if not deliveries:
            errors.append("❌ En az 1 teslimat noktası gerekli")
            return False, errors
        
        for delivery in deliveries:
            if delivery.weight <= 0:
                errors.append(f"❌ Teslimat {delivery.id}: Geçersiz ağırlık ({delivery.weight})")
            
            if not (1 <= delivery.priority <= 5):
                errors.append(f"❌ Teslimat {delivery.id}: Geçersiz öncelik ({delivery.priority})")
            
            # Pozisyon kontrolü
            x, y = delivery.pos
            if not (0 <= x <= 100) or not (0 <= y <= 100):
                errors.append(f"❌ Teslimat {delivery.id}: Geçersiz pozisyon ({x}, {y})")
            
            # Zaman penceresi kontrolü
            try:
                start_time, end_time = delivery.time_window
                if not isinstance(start_time, str) or not isinstance(end_time, str):
                    errors.append(f"❌ Teslimat {delivery.id}: Geçersiz zaman penceresi formatı")
            except:
                errors.append(f"❌ Teslimat {delivery.id}: Zaman penceresi formatı hatalı")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_no_fly_zones(no_fly_zones: List[NoFlyZone]) -> tuple[bool, List[str]]:
        """Yasak bölge verilerini doğrula"""
        errors = []
        warnings = []
        
        for nfz in no_fly_zones:
            if len(nfz.coordinates) < 3:
                errors.append(f"❌ Yasak Bölge {nfz.id}: En az 3 koordinat gerekli")
            
            # Koordinat kontrolü
            for i, (x, y) in enumerate(nfz.coordinates):
                if not (0 <= x <= 100) or not (0 <= y <= 100):
                    errors.append(f"❌ Yasak Bölge {nfz.id}: Geçersiz {i+1}. koordinat ({x}, {y})")
            
            # Zaman penceresi kontrolü
            try:
                start_time, end_time = nfz.active_time
                if not isinstance(start_time, str) or not isinstance(end_time, str):
                    errors.append(f"❌ Yasak Bölge {nfz.id}: Geçersiz zaman formatı")
            except:
                errors.append(f"❌ Yasak Bölge {nfz.id}: Zaman formatı hatalı")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_scenario_compatibility(drones: List[Drone], deliveries: List[DeliveryPoint]) -> tuple[bool, List[str]]:
        """Senaryo uyumluluğunu kontrol et"""
        errors = []
        warnings = []
        
        # Kapasitet analizi
        total_delivery_weight = sum(d.weight for d in deliveries)
        total_drone_capacity = sum(d.max_weight for d in drones)
        
        if total_delivery_weight > total_drone_capacity:
            errors.append(f"❌ Toplam teslimat ağırlığı ({total_delivery_weight:.2f}) drone kapasitesinden ({total_drone_capacity:.2f}) fazla")
        
        # Acil teslimat kontrolü
        urgent_deliveries = [d for d in deliveries if d.priority >= 4]
        if len(urgent_deliveries) > len(drones):
            warnings.append(f"⚠️ Acil teslimat sayısı ({len(urgent_deliveries)}) drone sayısından ({len(drones)}) fazla")
        
        # Zaman penceresi çakışma kontrolü
        overlapping_windows = 0
        for i in range(len(deliveries)):
            for j in range(i+1, len(deliveries)):
                # Basit zaman çakışma kontrolü (geliştirilmesi gerekebilir)
                d1, d2 = deliveries[i], deliveries[j]
                if d1.priority >= 4 and d2.priority >= 4:  # İki acil teslimat
                    overlapping_windows += 1
        
        if overlapping_windows > len(drones) // 2:
            warnings.append(f"⚠️ Çok sayıda acil teslimat çakışması tespit edildi ({overlapping_windows})")
        
        return len(errors) == 0, errors + warnings
    
    @staticmethod
    def validate_full_scenario(drones: List[Drone], deliveries: List[DeliveryPoint], no_fly_zones: List[NoFlyZone]) -> dict:
        """Tam senaryo doğrulaması"""
        print("🔍 Veri doğrulaması yapılıyor...")
        
        all_errors = []
        all_warnings = []
        
        # Ayrı ayrı doğrulama
        drone_valid, drone_errors = DataValidator.validate_drones(drones)
        delivery_valid, delivery_errors = DataValidator.validate_deliveries(deliveries)
        nfz_valid, nfz_errors = DataValidator.validate_no_fly_zones(no_fly_zones)
        compat_valid, compat_messages = DataValidator.validate_scenario_compatibility(drones, deliveries)
        
        all_errors.extend(drone_errors + delivery_errors + nfz_errors)
        
        # Uyumluluk mesajlarını ayır
        for msg in compat_messages:
            if msg.startswith("❌"):
                all_errors.append(msg)
            else:
                all_warnings.append(msg)
        
        is_valid = drone_valid and delivery_valid and nfz_valid and compat_valid
        
        # Sonuçları raporla
        if is_valid and not all_warnings:
            print("✅ Tüm veriler geçerli!")
        elif is_valid and all_warnings:
            print("✅ Veriler geçerli, ancak uyarılar var:")
            for warning in all_warnings:
                print(f"   {warning}")
        else:
            print("❌ Veri doğrulama hataları:")
            for error in all_errors:
                print(f"   {error}")
        
        return {
            'is_valid': is_valid,
            'errors': all_errors,
            'warnings': all_warnings,
            'summary': {
                'drones_valid': drone_valid,
                'deliveries_valid': delivery_valid,
                'no_fly_zones_valid': nfz_valid,
                'compatibility_valid': compat_valid
            }
        }