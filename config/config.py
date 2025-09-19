# config/config.py
"""Configuration file untuk weather info system"""

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

# Display Configuration
DISPLAY_CONFIG = {
    'datetime_format': '%Y%m%d_%H%M%S',
    'max_districts_display': 20,
    'decimal_places': 1
}

# Plotting Configuration
PLOT_CONFIG = {
    'style': 'seaborn-v0_8',
    'palette': 'husl',
    'figure_size': (18, 12),
    'dpi': 300,
    'backend': 'Agg'
}