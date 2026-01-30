#!/usr/bin/env python
"""Configurações centralizadas da aplicação."""

class Settings:
    """Configurações da aplicação."""
    
    page_title = "Analytics Pro - SaaS"
    layout = "wide"
    initial_sidebar_state = "expanded"
    app_version = "1.0.0"
    
    theme_vk_metrics = """
    <style>
        :root {
            --primary-color: #7C3AED;
            --secondary-color: #6D28D9;
        }
        
        .main {
            background-color: #0B0E14;
            color: #FFFFFF;
        }
        
        .stMetricValue {
            font-size: 28px;
            color: #7C3AED;
            font-weight: bold;
        }
        
        .stButton > button {
            background-color: #7C3AED;
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        }
        
        .stButton > button:hover {
            background-color: #6D28D9;
        }
    </style>
    """

settings = Settings()
