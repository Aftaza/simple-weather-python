# main.py
"""
Main application untuk Sistem Informasi Cuaca Jawa Timur
Menggunakan pola MVC (Model-View-Controller) dengan OOP
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from controllers.weather_controller import WeatherController
from utils.helpers import validate_api_key, ColoredOutput

def check_dependencies():
    """Cek dependencies yang diperlukan"""
    required_packages = {
        'pandas': 'pandas',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'requests': 'requests'
    }
    
    missing_packages = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            ColoredOutput.print_success(f"{package_name} tersedia")
        except ImportError:
            missing_packages.append(package_name)
            ColoredOutput.print_error(f"{package_name} tidak ditemukan")
    
    if missing_packages:
        ColoredOutput.print_error("Missing dependencies!")
        ColoredOutput.print_warning(f"Install dengan: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def get_api_key():
    """Mendapatkan API key dari user dengan validasi"""
    ColoredOutput.print_info("Untuk menggunakan aplikasi ini, Anda memerlukan API key dari WeatherAPI.com")
    ColoredOutput.print_info("Daftar gratis di: https://www.weatherapi.com/")
    print()
    
    while True:
        api_key = input("Masukkan API Key WeatherAPI.com: ").strip()
        
        if not api_key:
            ColoredOutput.print_error("API Key tidak boleh kosong!")
            continue
        
        if validate_api_key(api_key):
            return api_key
        else:
            ColoredOutput.print_error("Format API Key tidak valid!")

def show_welcome():
    """Menampilkan pesan selamat datang"""
    ColoredOutput.print_colored("=" * 60, 'CYAN')
    ColoredOutput.print_colored("🌤️  SISTEM INFORMASI CUACA JAWA TIMUR  🌤️", 'BOLD')
    ColoredOutput.print_colored("=" * 60, 'CYAN')
    ColoredOutput.print_colored("Dikembangkan dengan pola MVC dan OOP", 'MAGENTA')
    ColoredOutput.print_colored("Mendukung threading untuk performa optimal", 'MAGENTA')
    print()

def main():
    """Fungsi utama aplikasi"""
    try:
        # Show welcome message
        show_welcome()
        
        # Check dependencies
        ColoredOutput.print_info("Memeriksa dependencies...")
        if not check_dependencies():
            return
        
        print()
        ColoredOutput.print_success("Semua dependencies tersedia!")
        print()
        
        # Get API key
        api_key = get_api_key()
        
        # Initialize and run controller
        ColoredOutput.print_info("Menginisialisasi aplikasi...")
        controller = WeatherController(api_key)
        controller.run()
        
    except KeyboardInterrupt:
        print("\n")
        ColoredOutput.print_warning("Aplikasi dihentikan oleh user")
        ColoredOutput.print_info("Terima kasih telah menggunakan Sistem Informasi Cuaca!")
    except Exception as e:
        ColoredOutput.print_error(f"Terjadi kesalahan fatal: {e}")
        ColoredOutput.print_warning("Silakan coba lagi atau hubungi developer")
        input("Tekan Enter untuk keluar...")

if __name__ == "__main__":
    main()