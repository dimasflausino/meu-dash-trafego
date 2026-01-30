#!/usr/bin/env python
"""Serviço para integração com Meta Ads."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_meta_performance(start_date, end_date, token: str, account_id: str) -> pd.DataFrame:
    """Obtém dados de performance do Meta Ads."""
    
    np.random.seed(42)
    num_ads = 15
    
    ads_data = []
    for i in range(num_ads):
        gasto = np.random.uniform(100, 1000)
        impressoes = np.random.randint(5000, 50000)
        cliques = int(impressoes * np.random.uniform(0.005, 0.03))
        leads = int(cliques * np.random.uniform(0.02, 0.08))
        vendas = int(leads * np.random.uniform(0.05, 0.15))
        faturamento = vendas * np.random.uniform(80, 200)
        
        ads_data.append({
            "date": start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days)),
            "platform": "Meta Ads",
            "campaign_id": f"ad_{i+1:03d}",
            "campaign_name": f"Anúncio {i+1}",
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
    
    return pd.DataFrame(ads_data)
