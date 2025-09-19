# 🌤️ Sistem Informasi Cuaca Jawa Timur | Komputasi Paralel

![Project Status: In Development](https://img.shields.io/badge/status-in%20development-yellowgreen)
![Next.js](https://img.shields.io/badge/Python-13%2B-black?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-1-blue?logo=pandas)
![License: MIT](https://img.shields.io/badge/License-MIT-green)


Aplikasi Python untuk monitoring cuaca real-time di seluruh kecamatan Jawa Timur dengan menggunakan pola **MVC (Model-View-Controller)** dan **Object-Oriented Programming (OOP)**.

## ✨ Fitur Utama

- 📊 **Real-time Weather Data**: Data cuaca terkini untuk 20 kecamatan di Jawa Timur
- 🚀 **Multi-threading**: Pengambilan data secara paralel untuk performa optimal
- 📈 **Visualisasi Data**: Grafik dan chart interaktif menggunakan Matplotlib & Seaborn
- 💾 **Export Data**: Export data ke format CSV untuk analisis lebih lanjut
- 🔍 **Search & Filter**: Pencarian berdasarkan kondisi cuaca tertentu
- 📱 **User-friendly Interface**: Interface terminal yang intuitif dan mudah digunakan

## 🏗️ Arsitektur

Aplikasi ini menggunakan pola **MVC** dengan struktur sebagai berikut:

```
weather_info_system/
├── main.py                      # Entry point aplikasi
├── requirements.txt             # Dependencies
├── README.md                   # Documentation
├── config/
│   └── config.py              # Configuration settings
├── models/
│   ├── weather_data.py        # WeatherData dataclass
│   └── weather_model.py       # WeatherModel (business logic)
├── views/
│   └── weather_view.py        # WeatherView (presentation layer)
├── controllers/
│   └── weather_controller.py  # WeatherController (application logic)
├── services/
│   ├── weather_api.py         # WeatherAPIService (external API)
│   └── plot_service.py        # PlotService (plotting logic)
└── utils/
    └── helpers.py             # Utility functions
```

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Aftaza/simple-weather-python.git
cd simple-weather-python
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
> Tips: Bisa menggunakn virtual environtment agar lebih aman dari error konflik dependensi

### 3. Get API Key

- Daftar gratis di [WeatherAPI.com](https://www.weatherapi.com/)
- Dapatkan API key Anda

### 4. Run Application

```bash
python main.py
```

## 📋 Menu Aplikasi

1. **Lihat Cuaca Semua Kecamatan** - Overview cuaca seluruh Jawa Timur
2. **Lihat Cuaca Kecamatan Tertentu** - Detail cuaca per kecamatan
3. **Cari Cuaca Berdasarkan Kondisi** - Filter berdasarkan kondisi cuaca
4. **Statistik Cuaca & Grafik** - Analisis dan visualisasi data
5. **Export Data ke CSV** - Export data untuk analisis eksternal
6. **Refresh Data** - Update data terbaru
7. **Keluar** - Tutup aplikasi

## 🏛️ Komponen Arsitektur

### Models
- **`WeatherData`**: Dataclass untuk struktur data cuaca
- **`WeatherModel`**: Business logic dan data management menggunakan Pandas

### Views  
- **`WeatherView`**: Presentation layer untuk display terminal

### Controllers
- **`WeatherController`**: Application logic dan user interaction handling

### Services
- **`WeatherAPIService`**: External API communication dengan threading
- **`PlotService`**: Data visualization dan plotting

### Utils
- **`helpers.py`**: Utility functions dan helper classes

## 🔧 Konfigurasi

Edit file `config/config.py` untuk menyesuaikan:

```python
# API Configuration
API_CONFIG = {
    'base_url': "http://api.weatherapi.com/v1/current.json",
    'timeout': 10,
    'max_workers': 5
}

# File Configuration
FILE_CONFIG = {
    'csv_prefix': 'cuaca_jatim',
    'plot_prefix': 'grafik_cuaca_jatim',
    'encoding': 'utf-8'
}
```

## 📊 Data yang Dikumpulkan

- 🌡️ Suhu (°C)
- 🤒 Feels Like Temperature (°C)  
- 💧 Kelembaban (%)
- 💨 Kecepatan Angin (km/h)
- 🧭 Arah Angin
- ☁️ Kondisi Cuaca
- 👁️ Jarak Pandang (km)
- 🔽 Tekanan Udara (mb)
- ☀️ Indeks UV
- 🕒 Waktu Update Terakhir

## 🎯 Kecamatan yang Didukung

20 Kecamatan di Jawa Timur:
- Surabaya, Malang, Kediri, Blitar, Madiun
- Mojokerto, Pasuruan, Probolinggo, Sidoarjo, Gresik
- Jember, Banyuwangi, Tulungagung, Lumajang, Bondowoso
- Situbondo, Ngawi, Bojonegoro, Tuban, Lamongan

## 📈 Fitur Visualisasi

- **Histogram Suhu**: Distribusi suhu di seluruh kecamatan
- **Bar Chart Kondisi**: Kondisi cuaca tersering
- **Scatter Plot**: Korelasi suhu vs kelembaban
- **Box Plot Angin**: Distribusi kecepatan angin
- **Bar Chart Tekanan**: Ranking tekanan udara
- **Pie Chart UV Index**: Kategorisasi indeks UV

## 🛠️ Dependencies

- **pandas**: Data processing dan analysis
- **requests**: HTTP API calls
- **matplotlib**: Basic plotting
- **seaborn**: Statistical visualization
- **concurrent.futures**: Multi-threading
- **dataclasses**: Data structures

## 🔒 Error Handling

- ✅ Robust API error handling
- ✅ Network timeout handling
- ✅ Data validation
- ✅ Graceful degradation
- ✅ User input validation

## 🚀 Performance Features

- **Multi-threading**: Pengambilan data paralel
- **Efficient DataFrame operations**: Optimized dengan Pandas
- **Memory management**: Proper resource cleanup
- **Caching**: Data caching untuk mengurangi API calls

## 📝 Logging & Monitoring

- Real-time progress tracking
- Success/failure reporting
- Performance metrics
- Error logging

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.

## 👨‍💻 Developer

Dikembangkan dengan ❤️ menggunakan Python, Pandas, dan best practices OOP/MVC.

---

**Note**: Pastikan Anda memiliki koneksi internet yang stabil untuk mengakses WeatherAPI.com