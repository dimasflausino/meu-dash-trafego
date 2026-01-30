#!/usr/bin/env python
"""Serviço para integração com Hotmart."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_hotmart_sales(start_date, end_date, user_code: str, api_token: str) -> pd.DataFrame:
    """Obtém dados de vendas do Hotmart."""
    
    np.random.seed(789)
    num_products = 8
    
    products_data = []
    for i in range(num_products):
        vendas = np.random.randint(5, 50)
        preco_unitario = np.random.uniform(47, 297)
        faturamento = vendas * preco_unitario
        comissao = faturamento * 0.30
        lucro = faturamento - comissao
        
        products_data.append({
            "date": start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days)),
            "platform": "Hotmart",
            "product_id": f"prod_{i+1:03d}",
            "product_name": f"Produto {i+1}",
            "investment": 0,
            "impressions": 0,
            "clicks": 0,
            "leads": 0,
            "sales": vendas,
            "revenue": faturamento,
            "ctr": 0,
            "cpc": 0,
            "cpl": 0,
            "roi": ((lucro / faturamento) * 100) if faturamento > 0 else 0
        })
    
    return pd.DataFrame(products_data)
