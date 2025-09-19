# models/weather_data.py
from dataclasses import dataclass
from typing import Dict

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