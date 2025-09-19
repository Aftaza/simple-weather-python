# services/weather_api.py
import requests
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

class WeatherAPIService:
    """Service untuk mengambil data cuaca dari API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1/current.json"
        
        # Daftar kecamatan di Jawa Timur
        self.districts = {
            'Surabaya': ['Surabaya', 'East Java', 'Indonesia'],
            'Malang': ['Malang', 'East Java', 'Indonesia'],
            'Kediri': ['Kediri', 'East Java', 'Indonesia'],
            'Blitar': ['Blitar', 'East Java', 'Indonesia'],
            'Madiun': ['Madiun', 'East Java', 'Indonesia'],
            'Mojokerto': ['Mojokerto', 'East Java', 'Indonesia'],
            'Pasuruan': ['Pasuruan', 'East Java', 'Indonesia'],
            'Probolinggo': ['Probolinggo', 'East Java', 'Indonesia'],
            'Sidoarjo': ['Sidoarjo', 'East Java', 'Indonesia'],
            'Gresik': ['Gresik', 'East Java', 'Indonesia'],
            'Jember': ['Jember', 'East Java', 'Indonesia'],
            'Banyuwangi': ['Banyuwangi', 'East Java', 'Indonesia'],
            'Tulungagung': ['Tulungagung', 'East Java', 'Indonesia'],
            'Lumajang': ['Lumajang', 'East Java', 'Indonesia'],
            'Bondowoso': ['Bondowoso', 'East Java', 'Indonesia'],
            'Situbondo': ['Situbondo', 'East Java', 'Indonesia'],
            'Ngawi': ['Ngawi', 'East Java', 'Indonesia'],
            'Bojonegoro': ['Bojonegoro', 'East Java', 'Indonesia'],
            'Tuban': ['Tuban', 'East Java', 'Indonesia'],
            'Lamongan': ['Lamongan', 'East Java', 'Indonesia']
        }
    
    def fetch_weather_data(self, district: str, location_parts: List[str]) -> Optional[Dict]:
        """Mengambil data cuaca dari API untuk satu kecamatan"""
        try:
            location = f"{location_parts[0]}, {location_parts[1]}, {location_parts[2]}"
            params = {
                'key': self.api_key,
                'q': location,
                'aqi': 'no'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            current = data['current']
            location_info = data['location']
            
            weather_dict = {
                'location': location_info['name'],
                'district': district,
                'temperature': current['temp_c'],
                'feels_like': current['feelslike_c'],
                'humidity': current['humidity'],
                'wind_speed': current['wind_kph'],
                'wind_direction': current['wind_dir'],
                'condition': current['condition']['text'],
                'visibility': current['vis_km'],
                'pressure': current['pressure_mb'],
                'uv_index': current['uv'],
                'last_updated': current['last_updated']
            }
            
            return weather_dict
            
        except requests.RequestException as e:
            print(f"Error fetching data for {district}: {e}")
            return None
        except KeyError as e:
            print(f"Error parsing data for {district}: {e}")
            return None
    
    def fetch_all_weather_data_threaded(self, max_workers: int = 5) -> List[Dict]:
        """Mengambil data cuaca untuk semua kecamatan menggunakan threading"""
        print("Mengambil data cuaca untuk seluruh Jawa Timur...")
        
        weather_data_list = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit semua task
            future_to_district = {
                executor.submit(self.fetch_weather_data, district, location_parts): district
                for district, location_parts in self.districts.items()
            }
            
            # Collect results
            completed_count = 0
            total_count = len(self.districts)
            
            for future in as_completed(future_to_district):
                district = future_to_district[future]
                completed_count += 1
                
                try:
                    result = future.result()
                    if result:
                        weather_data_list.append(result)
                        print(f"✓ Data {district} berhasil diambil ({completed_count}/{total_count})")
                    else:
                        print(f"✗ Gagal mengambil data {district} ({completed_count}/{total_count})")
                except Exception as e:
                    print(f"✗ Error untuk {district}: {e} ({completed_count}/{total_count})")
        
        print(f"\nSelesai! Berhasil mengambil data {len(weather_data_list)} kecamatan")
        return weather_data_list