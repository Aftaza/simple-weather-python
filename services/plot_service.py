# services/plot_service.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set matplotlib to use non-interactive backend
plt.switch_backend('Agg')

class PlotService:
    """Service untuk membuat grafik dan visualisasi cuaca"""
    
    def __init__(self):
        # Set style untuk matplotlib
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def create_weather_plots(self, weather_df: pd.DataFrame) -> str:
        """Membuat grafik cuaca dan mengembalikan nama file"""
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
            
            return filename
            
        except Exception as e:
            raise Exception(f"Error membuat grafik: {e}")
    
    def get_weather_statistics(self, weather_df: pd.DataFrame) -> tuple:
        """Mendapatkan statistik cuaca untuk ditampilkan"""
        if weather_df.empty:
            return None, None
        
        # Statistik deskriptif
        numeric_cols = ['temperature', 'humidity', 'wind_speed', 'pressure', 'uv_index']
        stats_df = weather_df[numeric_cols].describe()
        
        # Kondisi cuaca paling umum
        condition_counts = weather_df['condition'].value_counts()
        
        return stats_df, condition_counts