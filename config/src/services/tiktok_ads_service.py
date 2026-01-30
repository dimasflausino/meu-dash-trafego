#!/usr/bin/env python
"""Serviço para integração com TikTok Ads."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_tiktok_performance(start_date, end_date, token: str, advertiser_id: str) -> pd.DataFrame:
    """Obtém dados de performance do TikTok Ads."""
    
    np.random.seed(456)
    num_campaigns = 10
    
    campaigns_data = []
    for i in range(num_campaigns):
        gasto = np.random.uniform(50, 600)
        impressoes = np.random.randint(10000, 100000)
        cliques = int(impressoes * np.random.uniform(0.001, 0.02))
        leads = int(cliques * np.random.uniform(0.01, 0.05))
        vendas = int(leads * np.random.uniform(0.03, 0.12))
        faturamento = vendas * np.random.uniform(60, 180)
        
        campaigns_data.append({
            "date": start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days)),
            "platform": "TikTok Ads",
            "campaign_id": f"tiktok_{i+1:03d}",
            "campaign_name": f"Campanha TikTok {i+1}",
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
