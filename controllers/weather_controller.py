# controllers/weather_controller.py
from models.weather_model import WeatherModel
from views.weather_view import WeatherView

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