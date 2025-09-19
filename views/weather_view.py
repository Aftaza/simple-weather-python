# views/weather_view.py
import pandas as pd
import os
from typing import List
from services.plot_service import PlotService

class WeatherView:
    """View untuk menampilkan informasi cuaca di terminal"""
    
    def __init__(self):
        self.plot_service = PlotService()
    
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
        
        # Mendapatkan statistik dari plot service
        stats_df, condition_counts = self.plot_service.get_weather_statistics(weather_df)
        
        print("📊 STATISTIK DESKRIPTIF:")
        print(stats_df.round(2).to_string())
        print()
        
        # Kondisi cuaca paling umum
        print("☁️ KONDISI CUACA TERSERING:")
        for condition, count in condition_counts.head().items():
            print(f"   {condition}: {count} kecamatan")
        print()
        
        if save_plots:
            try:
                filename = self.plot_service.create_weather_plots(weather_df)
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