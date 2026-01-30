#!/usr/bin/env python
"""
Serviço para integração com a API do Kiwify.

Este serviço é responsável por buscar dados de vendas, produtos e outras
informações da plataforma de infoprodutos Kiwify.

Versão atual: Utiliza dados simulados para desenvolvimento e testes sem custo.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_kiwify_performance(start_date: datetime, end_date: datetime, token: str, seller_id: str) -> pd.DataFrame:
    """
    Simula a busca de dados de performance do Kiwify.

    Em uma implementação real, esta função faria chamadas à API do Kiwify.
    Aqui, geramos um DataFrame com dados realistas para prototipação.

    Args:
        start_date: Data de início do período de análise.
        end_date: Data de fim do período de análise.
        token: Token de acesso à API (não utilizado na simulação).
        seller_id: ID do vendedor no Kiwify (não utilizado na simulação).

    Returns:
        Um DataFrame do Pandas com as métricas de performance simuladas.
    """
    # Simulação de dados
    date_range = pd.date_range(start_date, end_date)
    data = []

    for date in date_range:
        # Gera dados diários com uma variação aleatória
        vendas = np.random.randint(1, 10)
        faturamento = vendas * np.random.uniform(30, 150)
        comissao = faturamento * 0.15
        lucro = faturamento - comissao
        
        data.append({
            "date": date,
            "platform": "Kiwify",
            "sales": vendas,
            "revenue": faturamento,
            "commission": comissao,
            "profit": lucro
        })

    return pd.DataFrame(data)


def get_kiwify_products(start_date: datetime, end_date: datetime, token: str, seller_id: str) -> pd.DataFrame:
    """
    Retorna dados detalhados de produtos do Kiwify.
    """
    np.random.seed(654)
    num_products = 6
    
    products_data = []
    for i in range(num_products):
        vendas = np.random.randint(3, 30)
        preco_unitario = np.random.uniform(30, 150)
        faturamento = vendas * preco_unitario
        comissao_kiwify = faturamento * 0.15
        lucro_liquido = faturamento - comissao_kiwify
        
        products_data.append({
            "ID Produto": f"kiwify_{i+1:03d}",
            "Nome": f"Produto Kiwify {i+1}",
            "Tipo": np.random.choice(["Infoproduto", "Assinatura", "Serviço"]),
            "Vendas": vendas,
            "Preço Unitário": preco_unitario,
            "Faturamento": faturamento,
            "Comissão Kiwify": comissao_kiwify,
            "Lucro Líquido": lucro_liquido,
            "Taxa Conversão": np.random.uniform(0.5, 3)
        })
    
    return pd.DataFrame(products_data)
