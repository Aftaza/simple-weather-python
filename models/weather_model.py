# models/weather_model.py
import pandas as pd
import threading
import os  # <-- 1. Impor modul os
from datetime import datetime
from typing import Dict, Optional
from services.weather_api import WeatherAPIService

class WeatherModel:
    """Model untuk mengelola data cuaca menggunakan Pandas"""
    
    def __init__(self, api_key: str):
        self.api_service = WeatherAPIService(api_key)
        self.weather_df: pd.DataFrame = pd.DataFrame()
        self.lock = threading.Lock()
    
    def fetch_all_weather_data_threaded(self, max_workers: int = 5) -> pd.DataFrame:
        """Mengambil data cuaca untuk semua kecamatan menggunakan threading"""
        weather_data_list = self.api_service.fetch_all_weather_data_threaded(max_workers)
        
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
    
    def export_to_csv(self, filename: str = None) -> Optional[str]:
        """Export data ke file CSV di dalam folder 'data'."""
        
        folder_name = "data"
        
        os.makedirs(folder_name, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cuaca_jatim_{timestamp}.csv"
        
        file_path = os.path.join(folder_name, filename)
        
        with self.lock:
            if not self.weather_df.empty:
                # Reset index untuk export
                export_df = self.weather_df.reset_index()
                
                export_df.to_csv(file_path, index=False, encoding='utf-8')
                
                return file_path
        
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
    
    def get_districts(self) -> Dict:
        """Mendapatkan daftar kecamatan dari API service"""
        return self.api_service.districts