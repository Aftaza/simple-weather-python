# weather_info_system.py
import requests
import threading
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from typing import Dict, List, Optional
import os
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set matplotlib to use non-interactive backend
plt.switch_backend('Agg')

# =============================================================================
# MODEL CLASSES
# =============================================================================

@dataclass
class WeatherData:
    """Data class untuk menyimpan informasi cuaca"""
    location: str
    district: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    wind_direction: str
    condition: str
    visibility: float
    pressure: float
    uv_index: float
    last_updated: str
    
    def to_dict(self) -> Dict:
        return {
            'location': self.location,
            'district': self.district,
            'temperature': self.temperature,
            'feels_like': self.feels_like,
            'humidity': self.humidity,
            'wind_speed': self.wind_speed,
            'wind_direction': self.wind_direction,
            'condition': self.condition,
            'visibility': self.visibility,
            'pressure': self.pressure,
            'uv_index': self.uv_index,
            'last_updated': self.last_updated
        }

class WeatherModel:
    """Model untuk mengelola data cuaca menggunakan Pandas"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1/current.json"
        self.weather_df: pd.DataFrame = pd.DataFrame()
        self.lock = threading.Lock()
        
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
    
    def fetch_all_weather_data_threaded(self, max_workers: int = 5) -> pd.DataFrame:
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
        
        # Konversi ke DataFrame
        with self.lock:
            self.weather_df = pd.DataFrame(weather_data_list)
            if not self.weather_df.empty:
                # Set district sebagai index untuk akses mudah
                self.weather_df.set_index('district', inplace=True)
                # Convert numeric columns
                numeric_cols = ['temperature', 'feels_like', 'humidity', 'wind_speed', 
                               'visibility', 'pressure', 'uv_index']
                for col in numeric_cols:
                    if col in self.weather_df.columns:
                        self.weather_df[col] = pd.to_numeric(self.weather_df[col], errors='coerce')
                
                # Convert datetime
                self.weather_df['last_updated'] = pd.to_datetime(self.weather_df['last_updated'])
        
        print(f"\nSelesai! Berhasil mengambil data {len(self.weather_df)} kecamatan")
        return self.weather_df
    
    def get_weather_dataframe(self) -> pd.DataFrame:
        """Mendapatkan DataFrame cuaca"""
        with self.lock:
            return self.weather_df.copy()
    
    def get_weather_data(self, district: str = None) -> Optional[pd.Series]:
        """Mendapatkan data cuaca untuk kecamatan tertentu"""
        with self.lock:
            if district and district in self.weather_df.index:
                return self.weather_df.loc[district]
            return None
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export data ke file CSV"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cuaca_jatim_{timestamp}.csv"
        
        with self.lock:
            if not self.weather_df.empty:
                # Reset index untuk export
                export_df = self.weather_df.reset_index()
                export_df.to_csv(filename, index=False, encoding='utf-8')
                return filename
        return None
    
    def get_statistics(self) -> Dict:
        """Mendapatkan statistik cuaca"""
        with self.lock:
            if self.weather_df.empty:
                return {}
            
            numeric_cols = ['temperature', 'feels_like', 'humidity', 'wind_speed', 
                           'visibility', 'pressure', 'uv_index']
            stats = {}
            
            for col in numeric_cols:
                if col in self.weather_df.columns:
                    stats[col] = {
                        'mean': self.weather_df[col].mean(),
                        'min': self.weather_df[col].min(),
                        'max': self.weather_df[col].max(),
                        'std': self.weather_df[col].std(),
                        'median': self.weather_df[col].median()
                    }
            
            return stats

# =============================================================================
# VIEW CLASSES
# =============================================================================

class WeatherView:
    """View untuk menampilkan informasi cuaca di terminal"""
    
    def __init__(self):
        # Set style untuk matplotlib
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    @staticmethod
    def clear_screen():
        """Membersihkan layar terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def show_header():
        """Menampilkan header aplikasi"""
        print("=" * 60)
        print("🌤️  SISTEM INFORMASI CUACA JAWA TIMUR  🌤️")
        print("=" * 60)
        print()
    
    @staticmethod
    def show_main_menu():
        """Menampilkan menu utama"""
        print("📋 MENU UTAMA:")
        print("1. Lihat Cuaca Semua Kecamatan")
        print("2. Lihat Cuaca Kecamatan Tertentu")
        print("3. Cari Cuaca Berdasarkan Kondisi")
        print("4. Statistik Cuaca & Grafik")
        print("5. Export Data ke CSV")
        print("6. Refresh Data")
        print("7. Keluar")
        print("-" * 40)
    
    @staticmethod
    def show_weather_summary(weather_df: pd.DataFrame):
        """Menampilkan ringkasan cuaca semua kecamatan"""
        if weather_df.empty:
            print("❌ Tidak ada data cuaca tersedia")
            return
        
        print(f"📊 RINGKASAN CUACA JAWA TIMUR ({len(weather_df)} Kecamatan)")
        print("=" * 80)
        
        # Tampilkan DataFrame dengan formatting
        display_cols = ['location', 'temperature', 'condition', 'humidity', 'wind_speed']
        display_df = weather_df[display_cols].copy()
        
        # Format columns
        display_df['temperature'] = display_df['temperature'].apply(lambda x: f"{x}°C")
        display_df['humidity'] = display_df['humidity'].apply(lambda x: f"{x}%")
        display_df['wind_speed'] = display_df['wind_speed'].apply(lambda x: f"{x} km/h")
        
        # Rename columns for display
        display_df.columns = ['Lokasi', 'Suhu', 'Kondisi', 'Kelembaban', 'Angin']
        
        print(display_df.to_string(max_rows=None, max_cols=None))
    
    @staticmethod
    def show_detailed_weather(data: pd.Series, district: str):
        """Menampilkan informasi cuaca detail untuk satu kecamatan"""
        print(f"🌡️  DETAIL CUACA - {district.upper()}")
        print("=" * 50)
        print(f"📍 Lokasi          : {data['location']}")
        print(f"🌡️  Suhu            : {data['temperature']:.1f}°C")
        print(f"🤒 Terasa Seperti   : {data['feels_like']:.1f}°C")
        print(f"☁️  Kondisi         : {data['condition']}")
        print(f"💧 Kelembaban       : {data['humidity']}%")
        print(f"💨 Kecepatan Angin  : {data['wind_speed']:.1f} km/h ({data['wind_direction']})")
        print(f"👁️  Jarak Pandang   : {data['visibility']:.1f} km")
        print(f"🔽 Tekanan Udara    : {data['pressure']:.1f} mb")
        print(f"☀️  Indeks UV       : {data['uv_index']:.1f}")
        print(f"🕒 Terakhir Update  : {data['last_updated']}")
        print("=" * 50)
    
    @staticmethod
    def show_districts_list(districts: List[str]):
        """Menampilkan daftar kecamatan"""
        print("📍 DAFTAR KECAMATAN:")
        for i, district in enumerate(districts, 1):
            print(f"{i:2d}. {district}")
    
    def show_weather_statistics(self, weather_df: pd.DataFrame, save_plots: bool = True):
        """Menampilkan statistik cuaca dengan grafik"""
        if weather_df.empty:
            print("❌ Tidak ada data untuk statistik")
            return
        
        print("📈 STATISTIK CUACA JAWA TIMUR")
        print("=" * 50)
        
        # Statistik deskriptif
        numeric_cols = ['temperature', 'humidity', 'wind_speed', 'pressure', 'uv_index']
        stats_df = weather_df[numeric_cols].describe()
        
        print("📊 STATISTIK DESKRIPTIF:")
        print(stats_df.round(2).to_string())
        print()
        
        # Kondisi cuaca paling umum
        condition_counts = weather_df['condition'].value_counts()
        print("☁️ KONDISI CUACA TERSERING:")
        for condition, count in condition_counts.head().items():
            print(f"   {condition}: {count} kecamatan")
        print()
        
        if save_plots:
            self._create_weather_plots(weather_df)
    
    def _create_weather_plots(self, weather_df: pd.DataFrame):
        """Membuat grafik cuaca"""
        try:
            # Create figure dengan subplots
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('Analisis Cuaca Jawa Timur', fontsize=16, fontweight='bold')
            
            # 1. Histogram Suhu
            axes[0,0].hist(weather_df['temperature'], bins=10, alpha=0.7, color='orange', edgecolor='black')
            axes[0,0].set_title('Distribusi Suhu')
            axes[0,0].set_xlabel('Suhu (°C)')
            axes[0,0].set_ylabel('Jumlah Kecamatan')
            axes[0,0].grid(True, alpha=0.3)
            
            # 2. Bar chart kondisi cuaca
            condition_counts = weather_df['condition'].value_counts().head(8)
            axes[0,1].bar(range(len(condition_counts)), condition_counts.values, color='skyblue', edgecolor='black')
            axes[0,1].set_title('Kondisi Cuaca Tersering')
            axes[0,1].set_xlabel('Kondisi Cuaca')
            axes[0,1].set_ylabel('Jumlah Kecamatan')
            axes[0,1].set_xticks(range(len(condition_counts)))
            axes[0,1].set_xticklabels(condition_counts.index, rotation=45, ha='right')
            axes[0,1].grid(True, alpha=0.3)
            
            # 3. Scatter plot Suhu vs Kelembaban
            axes[0,2].scatter(weather_df['temperature'], weather_df['humidity'], 
                            alpha=0.7, color='red', s=60, edgecolors='black')
            axes[0,2].set_title('Suhu vs Kelembaban')
            axes[0,2].set_xlabel('Suhu (°C)')
            axes[0,2].set_ylabel('Kelembaban (%)')
            axes[0,2].grid(True, alpha=0.3)
            
            # 4. Box plot kecepatan angin
            axes[1,0].boxplot(weather_df['wind_speed'], patch_artist=True,
                            boxprops=dict(facecolor='lightgreen', alpha=0.7))
            axes[1,0].set_title('Distribusi Kecepatan Angin')
            axes[1,0].set_ylabel('Kecepatan Angin (km/h)')
            axes[1,0].grid(True, alpha=0.3)
            
            # 5. Bar chart tekanan udara per kecamatan (top 10)
            top_pressure = weather_df.nlargest(10, 'pressure')
            axes[1,1].barh(range(len(top_pressure)), top_pressure['pressure'], 
                          color='purple', alpha=0.7, edgecolor='black')
            axes[1,1].set_title('Top 10 Tekanan Udara Tertinggi')
            axes[1,1].set_xlabel('Tekanan (mb)')
            axes[1,1].set_ylabel('Kecamatan')
            axes[1,1].set_yticks(range(len(top_pressure)))
            axes[1,1].set_yticklabels(top_pressure.index)
            axes[1,1].grid(True, alpha=0.3)
            
            # 6. Pie chart indeks UV
            uv_ranges = pd.cut(weather_df['uv_index'], bins=[0, 3, 6, 8, 11, float('inf')], 
                              labels=['Rendah (0-3)', 'Sedang (3-6)', 'Tinggi (6-8)', 
                                     'Sangat Tinggi (8-11)', 'Ekstrem (>11)'])
            uv_counts = uv_ranges.value_counts()
            
            colors = ['green', 'yellow', 'orange', 'red', 'purple']
            axes[1,2].pie(uv_counts.values, labels=uv_counts.index, autopct='%1.1f%%',
                         colors=colors[:len(uv_counts)], startangle=90)
            axes[1,2].set_title('Distribusi Indeks UV')
            
            # Adjust layout
            plt.tight_layout()
            
            # Save plot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"grafik_cuaca_jatim_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📊 Grafik berhasil disimpan: {filename}")
            
        except Exception as e:
            print(f"❌ Error membuat grafik: {e}")
    
    @staticmethod
    def show_weather_by_condition(weather_df: pd.DataFrame, condition: str):
        """Menampilkan cuaca berdasarkan kondisi tertentu"""
        filtered_df = weather_df[weather_df['condition'].str.contains(condition, case=False, na=False)]
        
        if filtered_df.empty:
            print(f"❌ Tidak ditemukan kecamatan dengan kondisi '{condition}'")
            return
        
        print(f"🔍 KECAMATAN DENGAN KONDISI '{condition.upper()}':")
        print("=" * 60)
        
        for district, row in filtered_df.iterrows():
            print(f"📍 {district:<15} - {row['condition']} ({row['temperature']:.1f}°C)")
    
    @staticmethod
    def show_loading():
        """Menampilkan animasi loading"""
        print("⏳ Memuat data cuaca...")
    
    @staticmethod
    def show_error(message: str):
        """Menampilkan pesan error"""
        print(f"❌ Error: {message}")
    
    @staticmethod
    def show_success(message: str):
        """Menampilkan pesan sukses"""
        print(f"✅ {message}")

# =============================================================================
# CONTROLLER CLASS
# =============================================================================

class WeatherController:
    """Controller untuk mengelola logika aplikasi"""
    
    def __init__(self, api_key: str):
        self.model = WeatherModel(api_key)
        self.view = WeatherView()
        self.running = True
    
    def run(self):
        """Menjalankan aplikasi utama"""
        self.view.clear_screen()
        self.view.show_header()
        
        # Load data awal
        self.view.show_loading()
        self.model.fetch_all_weather_data_threaded()
        
        while self.running:
            self.view.clear_screen()
            self.view.show_header()
            self.view.show_main_menu()
            
            try:
                choice = input("Pilih menu (1-7): ").strip()
                self.handle_menu_choice(choice)
            except KeyboardInterrupt:
                print("\n\n👋 Terima kasih telah menggunakan sistem informasi cuaca!")
                break
            except Exception as e:
                self.view.show_error(f"Terjadi kesalahan: {e}")
                input("\nTekan Enter untuk melanjutkan...")
    
    def handle_menu_choice(self, choice: str):
        """Menangani pilihan menu"""
        if choice == '1':
            self.show_all_weather()
        elif choice == '2':
            self.show_specific_weather()
        elif choice == '3':
            self.search_weather_by_condition()
        elif choice == '4':
            self.show_statistics()
        elif choice == '5':
            self.export_data()
        elif choice == '6':
            self.refresh_data()
        elif choice == '7':
            self.running = False
            print("\n👋 Terima kasih telah menggunakan sistem informasi cuaca!")
        else:
            self.view.show_error("Pilihan tidak valid!")
            input("\nTekan Enter untuk melanjutkan...")
    
    def show_all_weather(self):
        """Menampilkan cuaca semua kecamatan"""
        self.view.clear_screen()
        self.view.show_header()
        
        weather_df = self.model.get_weather_dataframe()
        self.view.show_weather_summary(weather_df)
        
        input("\nTekan Enter untuk kembali ke menu...")
    
    def show_specific_weather(self):
        """Menampilkan cuaca kecamatan tertentu"""
        self.view.clear_screen()
        self.view.show_header()
        
        weather_df = self.model.get_weather_dataframe()
        if weather_df.empty:
            self.view.show_error("Tidak ada data cuaca tersedia")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        districts = list(weather_df.index)
        self.view.show_districts_list(districts)
        
        try:
            choice = input("\nPilih nomor kecamatan (atau ketik nama): ").strip()
            
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(districts):
                    district = districts[index]
                else:
                    raise ValueError("Nomor tidak valid")
            else:
                # Cari berdasarkan nama
                district = None
                for d in districts:
                    if choice.lower() in d.lower():
                        district = d
                        break
                if not district:
                    raise ValueError("Kecamatan tidak ditemukan")
            
            weather_data = self.model.get_weather_data(district)
            if weather_data is not None:
                self.view.clear_screen()
                self.view.show_header()
                self.view.show_detailed_weather(weather_data, district)
            else:
                self.view.show_error(f"Data cuaca untuk {district} tidak tersedia")
                
        except ValueError as e:
            self.view.show_error(str(e))
        
        input("\nTekan Enter untuk kembali ke menu...")
    
    def search_weather_by_condition(self):
        """Mencari cuaca berdasarkan kondisi"""
        self.view.clear_screen()
        self.view.show_header()
        
        condition = input("Masukkan kondisi cuaca yang dicari (misal: Cloudy, Sunny, Rain): ").strip()
        
        if condition:
            weather_df = self.model.get_weather_dataframe()
            self.view.show_weather_by_condition(weather_df, condition)
        else:
            self.view.show_error("Kondisi cuaca tidak boleh kosong")
        
        input("\nTekan Enter untuk kembali ke menu...")
    
    def show_statistics(self):
        """Menampilkan statistik cuaca dengan grafik"""
        self.view.clear_screen()
        self.view.show_header()
        
        weather_df = self.model.get_weather_dataframe()
        if weather_df.empty:
            self.view.show_error("Tidak ada data untuk statistik")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        print("📊 PILIHAN STATISTIK:")
        print("1. Tampilkan statistik saja")
        print("2. Tampilkan statistik + buat grafik")
        
        choice = input("\nPilih opsi (1-2): ").strip()
        
        if choice == '1':
            self.view.show_weather_statistics(weather_df, save_plots=False)
        elif choice == '2':
            self.view.show_weather_statistics(weather_df, save_plots=True)
        else:
            self.view.show_error("Pilihan tidak valid")
        
        input("\nTekan Enter untuk kembali ke menu...")
    
    def export_data(self):
        """Export data ke CSV"""
        self.view.clear_screen()
        self.view.show_header()
        
        weather_df = self.model.get_weather_dataframe()
        if weather_df.empty:
            self.view.show_error("Tidak ada data untuk di-export")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        print("💾 EXPORT DATA KE CSV")
        print("=" * 30)
        
        custom_name = input("Masukkan nama file (kosong untuk otomatis): ").strip()
        filename = custom_name if custom_name else None
        
        exported_file = self.model.export_to_csv(filename)
        
        if exported_file:
            self.view.show_success(f"Data berhasil di-export ke: {exported_file}")
            print(f"📁 File berisi {len(weather_df)} record data cuaca")
        else:
            self.view.show_error("Gagal export data")
        
        input("\nTekan Enter untuk kembali ke menu...")
    
    def refresh_data(self):
        """Refresh data cuaca"""
        self.view.clear_screen()
        self.view.show_header()
        self.view.show_loading()
        
        # Refresh data dengan threading
        self.model.fetch_all_weather_data_threaded()
        self.view.show_success("Data cuaca berhasil diperbarui!")
        
        input("\nTekan Enter untuk kembali ke menu...")

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Fungsi utama aplikasi"""
    print("🌤️  Sistem Informasi Cuaca Jawa Timur")
    print("=" * 40)
    
    # Cek dependencies
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        print("✅ Dependencies berhasil dimuat")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install dengan: pip install pandas matplotlib seaborn requests")
        return
    
    # Minta API key dari user
    api_key = input("\nMasukkan API Key WeatherAPI.com: ").strip()
    
    if not api_key:
        print("❌ API Key tidak boleh kosong!")
        return
    
    try:
        # Inisialisasi controller dan jalankan aplikasi
        controller = WeatherController(api_key)
        controller.run()
    except Exception as e:
        print(f"❌ Terjadi kesalahan fatal: {e}")
        input("Tekan Enter untuk keluar...")

if __name__ == "__main__":
    main()