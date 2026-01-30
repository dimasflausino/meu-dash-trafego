#!/usr/bin/env python
"""
Serviço para integração com a API do Google Ads.

Este serviço é responsável por buscar dados de campanhas, performance e outras
informações da plataforma de anúncios do Google (Search, Display, Shopping).

Versão atual: Utiliza dados simulados para desenvolvimento e testes sem custo.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_google_performance(start_date: datetime, end_date: datetime, token: str, customer_id: str) -> pd.DataFrame:
    """
    Simula a busca de dados de performance do Google Ads.

    Em uma implementação real, esta função faria chamadas à API do Google Ads.
    Aqui, geramos um DataFrame com dados realistas para prototipação.

    Args:
        start_date: Data de início do período de análise.
        end_date: Data de fim do período de análise.
        token: Token de acesso à API (não utilizado na simulação).
        customer_id: ID do cliente do Google Ads (não utilizado na simulação).

    Returns:
        Um DataFrame do Pandas com as métricas de performance simuladas.
    """
    # Simulação de dados
    date_range = pd.date_range(start_date, end_date)
    data = []

    for date in date_range:
        # Gera dados diários com uma variação aleatória
        investimento = np.random.uniform(80, 400)
        impressoes = np.random.randint(3000, 25000)
        cliques = impressoes * np.random.uniform(0.01, 0.05)
        vendas = cliques * np.random.uniform(0.03, 0.08)
        faturamento = vendas * np.random.uniform(100, 250)
        
        data.append({
            "date": date,
            "platform": "Google Ads",
            "investment": investimento,
            "impressions": int(impressoes),
            "clicks": int(cliques),
            "sales": int(vendas),
            "revenue": faturamento
        })

    return pd.DataFrame(data)


def get_google_campaigns(start_date: datetime, end_date: datetime, token: str, customer_id: str) -> pd.DataFrame:
    """
    Retorna dados detalhados de campanhas do Google Ads.
    """
    np.random.seed(456)
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
            "ID Campanha": f"camp_{i+1:03d}",
            "Nome": f"Campanha {i+1}",
            "Tipo": np.random.choice(["Search", "Display", "Shopping"]),
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
