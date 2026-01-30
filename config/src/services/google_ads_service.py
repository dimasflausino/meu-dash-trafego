#!/usr/bin/env python
"""Serviço para integração com Google Ads."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_google_performance(start_date, end_date, dev_token: str, customer_id: str) -> pd.DataFrame:
    """Obtém dados de performance do Google Ads."""
    
    np.random.seed(123)
    num_campaigns = 12
    
    campaigns_data = []
    for i in range(num_campaigns):
        gasto = np.random.uniform(80, 800)
        impressoes = np.random.randint(3000, 40000)
        cliques = int(impressoes * np.random.uniform(0.01, 0.04))
        leads = int(cliques * np.random.uniform(0.03, 0.10))
        vendas = int(leads * np.random.uniform(0.08, 0.20))
        faturamento = vendas * np.random.uniform(100, 250)
        
        campaigns_data.append({
            "date": start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days)),
            "platform": "Google Ads",
            "campaign_id": f"camp_{i+1:03d}",
            "campaign_name": f"Campanha {i+1}",
            "investment": gasto,
            "impressions": impressoes,
            "clicks": cliques,
            "leads": leads,
            "sales": vendas,
            "revenue": faturamento,
            "ctr": (cliques / impressoes * 100) if impressoes > 0 else 0,
            "cpc": (gasto / cliques) if cliques > 0 else 0,
            "cpl": (gasto / leads) if leads > 0 else 0,
            "roi": ((faturamento - gasto) / gasto * 100) if gasto > 0 else 0
        })
    
    return pd.DataFrame(campaigns_data)
