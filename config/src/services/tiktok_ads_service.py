#!/usr/bin/env python
"""
Serviço para integração com a API do TikTok Ads.

Este serviço é responsável por buscar dados de campanhas, performance e outras
informações da plataforma de anúncios do TikTok.

Versão atual: Utiliza dados simulados para desenvolvimento e testes sem custo.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_tiktok_performance(start_date: datetime, end_date: datetime, token: str, advertiser_id: str) -> pd.DataFrame:
    """
    Simula a busca de dados de performance do TikTok Ads.

    Em uma implementação real, esta função faria chamadas à API do TikTok Ads.
    Aqui, geramos um DataFrame com dados realistas para prototipação.

    Args:
        start_date: Data de início do período de análise.
        end_date: Data de fim do período de análise.
        token: Token de acesso à API (não utilizado na simulação).
        advertiser_id: ID do anunciante do TikTok (não utilizado na simulação).

    Returns:
        Um DataFrame do Pandas com as métricas de performance simuladas.
    """
    # Simulação de dados
    date_range = pd.date_range(start_date, end_date)
    data = []

    for date in date_range:
        # Gera dados diários com uma variação aleatória
        investimento = np.random.uniform(50, 300)
        impressoes = np.random.randint(10000, 100000)
        cliques = impressoes * np.random.uniform(0.001, 0.02)
        vendas = cliques * np.random.uniform(0.01, 0.05)
        faturamento = vendas * np.random.uniform(60, 180)
        
        data.append({
            "date": date,
            "platform": "TikTok Ads",
            "investment": investimento,
            "impressions": int(impressoes),
            "clicks": int(cliques),
            "sales": int(vendas),
            "revenue": faturamento
        })

    return pd.DataFrame(data)


def get_tiktok_campaigns(start_date: datetime, end_date: datetime, token: str, advertiser_id: str) -> pd.DataFrame:
    """
    Retorna dados detalhados de campanhas do TikTok Ads.
    """
    np.random.seed(789)
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
            "ID Campanha": f"tiktok_{i+1:03d}",
            "Nome": f"Campanha TikTok {i+1}",
            "Objetivo": np.random.choice(["Tráfego", "Conversão", "Reconhecimento"]),
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
    
    return pd.DataFrame(campaigns_data)
