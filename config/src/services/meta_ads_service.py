#!/usr/bin/env python
"""
Serviço para integração com a API do Meta Ads.

Este serviço é responsável por buscar dados de campanhas, performance e outras
informações da plataforma de anúncios da Meta (Facebook e Instagram).

Versão atual: Utiliza dados simulados para desenvolvimento e testes sem custo.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_meta_performance(start_date: datetime, end_date: datetime, token: str, account_id: str) -> pd.DataFrame:
    """
    Simula a busca de dados de performance do Meta Ads.

    Em uma implementação real, esta função faria chamadas à API Graph do Facebook.
    Aqui, geramos um DataFrame com dados realistas para prototipação.

    Args:
        start_date: Data de início do período de análise.
        end_date: Data de fim do período de análise.
        token: Token de acesso à API (não utilizado na simulação).
        account_id: ID da conta de anúncios (não utilizado na simulação).

    Returns:
        Um DataFrame do Pandas com as métricas de performance simuladas.
    """
    # Simulação de dados
    date_range = pd.date_range(start_date, end_date)
    data = []

    for date in date_range:
        # Gera dados diários com uma variação aleatória
        investimento = np.random.uniform(100, 500)
        impressoes = np.random.randint(5000, 20000)
        cliques = impressoes * np.random.uniform(0.01, 0.03)
        vendas = cliques * np.random.uniform(0.02, 0.05)
        faturamento = vendas * np.random.uniform(80, 150)
        
        data.append({
            "date": date,
            "platform": "Meta Ads",
            "investment": investimento,
            "impressions": int(impressoes),
            "clicks": int(cliques),
            "sales": int(vendas),
            "revenue": faturamento
        })

    return pd.DataFrame(data)


def get_meta_ads(start_date: datetime, end_date: datetime, token: str, account_id: str) -> pd.DataFrame:
    """
    Retorna dados detalhados de anúncios do Meta Ads.
    """
    np.random.seed(123)
    num_ads = 15
    
    ads_data = []
    for i in range(num_ads):
        gasto = np.random.uniform(50, 500)
        impressoes = np.random.randint(2000, 15000)
        cliques = int(impressoes * np.random.uniform(0.01, 0.04))
        leads = int(cliques * np.random.uniform(0.02, 0.08))
        vendas = int(leads * np.random.uniform(0.05, 0.15))
        faturamento = vendas * np.random.uniform(70, 200)
        
        ads_data.append({
            "ID Anúncio": f"ad_{i+1:03d}",
            "Nome": f"Anúncio {i+1}",
            "Status": np.random.choice(["Ativo", "Pausado"]),
            "Gasto": gasto,
            "Impressões": impressoes,
            "Cliques": cliques,
            "CTR": (cliques / impressoes * 100) if impressoes > 0 else 0,
            "CPC": (gasto / cliques) if cliques > 0 else 0,
            "Leads": leads,
            "CPL": (gasto / leads) if leads > 0 else 0,
            "Vendas": vendas,
            "Faturamento": faturamento,
            "ROI": ((faturamento - gasto) / gasto * 100) if gasto > 0 else 0
        })
    
    return pd.DataFrame(ads_data)
