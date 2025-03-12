from SensorReading import VL53
import serial
import time

class SensorManager:
    _instance = None  # Tek örneği saklayacak değişken

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SensorManager, cls).__new__(cls, *args, **kwargs)
            print("SensorManager instance created.")
            cls._instance.initialize_sensors()  # Sensörleri başlat
        return cls._instance

    def initialize_sensors(self):
        """Sensörleri başlatma fonksiyonu"""
        self.sensors = {"sensor1": 0, "sensor2": 0}  # Varsayılan sensör değerleri
        print("Sensors initialized.")

    def read_sensor(self, sensor_name):
        """Belirtilen sensörden veri oku (Örnek olarak rastgele veri üretelim)"""
        if sensor_name in self.sensors:
            self.sensors[sensor_name] = time.time() % 100  # Örnek olarak zaman bazlı bir değer atıyoruz
            return self.sensors[sensor_name]
        else:
            raise ValueError(f"Sensor {sensor_name} not found!")

    def get_all_sensors(self):
        """Tüm sensör değerlerini döndür"""
        return self.sensors

    def close_sensors(self):
        """Sensörleri kapatma fonksiyonu"""
        print("Closing all sensors...")
        self.sensors = {}  # Sensörleri temizle

# Kullanım:
sensor_manager1 = SensorManager()
sensor_manager2 = SensorManager()

print(sensor_manager1 is sensor_manager2)  # True dönecek, çünkü Singleton deseni uygulanıyor

print(sensor_manager1.read_sensor("sensor1"))  # Sensor1 değerini oku
print(sensor_manager2.get_all_sensors())  # Aynı instance üzerinden tüm sensör değerlerini al
