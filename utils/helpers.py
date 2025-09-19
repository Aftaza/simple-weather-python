# utils/helpers.py
"""Utility functions untuk weather info system"""

import os
from datetime import datetime
from typing import List, Dict, Any

def clear_screen():
    """Cross-platform screen clearing"""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_timestamp_filename(prefix: str, extension: str = '.csv') -> str:
    """Generate filename dengan timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}{extension}"

def format_temperature(temp: float, decimal_places: int = 1) -> str:
    """Format temperature untuk display"""
    return f"{temp:.{decimal_places}f}°C"

def format_percentage(value: float) -> str:
    """Format percentage untuk display"""
    return f"{value}%"

def format_speed(speed: float, unit: str = "km/h") -> str:
    """Format speed untuk display"""
    return f"{speed} {unit}"

def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    return bool(api_key and isinstance(api_key, str) and len(api_key.strip()) > 0)

def safe_float_conversion(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int_conversion(value: Any, default: int = 0) -> int:
    """Safely convert value to int"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def format_file_size(file_path: str) -> str:
    """Get formatted file size"""
    try:
        size_bytes = os.path.getsize(file_path)
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    except OSError:
        return "Unknown size"

def get_districts_by_search(districts: List[str], search_term: str) -> List[str]:
    """Search districts by term"""
    search_term = search_term.lower()
    return [d for d in districts if search_term in d.lower()]

class ColoredOutput:
    """Class untuk colored terminal output"""
    
    COLORS = {
        'RED': '\033[91m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'BLUE': '\033[94m',
        'MAGENTA': '\033[95m',
        'CYAN': '\033[96m',
        'WHITE': '\033[97m',
        'ENDC': '\033[0m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m'
    }
    
    @classmethod
    def print_colored(cls, text: str, color: str = 'WHITE'):
        """Print colored text"""
        color_code = cls.COLORS.get(color.upper(), cls.COLORS['WHITE'])
        print(f"{color_code}{text}{cls.COLORS['ENDC']}")
    
    @classmethod
    def print_success(cls, text: str):
        """Print success message"""
        cls.print_colored(f"✅ {text}", 'GREEN')
    
    @classmethod
    def print_error(cls, text: str):
        """Print error message"""
        cls.print_colored(f"❌ {text}", 'RED')
    
    @classmethod
    def print_warning(cls, text: str):
        """Print warning message"""
        cls.print_colored(f"⚠️ {text}", 'YELLOW')
    
    @classmethod
    def print_info(cls, text: str):
        """Print info message"""
        cls.print_colored(f"ℹ️ {text}", 'BLUE')