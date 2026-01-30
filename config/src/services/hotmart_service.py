#!/usr/bin/env python
"""
Serviço para integração com a API do Hotmart.

Este serviço é responsável por buscar dados de vendas, produtos e outras
informações da plataforma de infoprodutos Hotmart.

Versão atual: Utiliza dados simulados para desenvolvimento e testes sem custo.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_hotmart_performance(start_date: datetime, end_date: datetime, token: str, producer_id: str) -> pd.DataFrame:
    """
    Simula a busca de dados de performance do Hotmart.

    Em uma implementação real, esta função faria chamadas à API do Hotmart.
    Aqui, geramos um DataFrame com dados realistas para prototipação.

    Args:
        start_date: Data de início do período de análise.
        end_date: Data de fim do período de análise.
        token: Token de acesso à API (não utilizado na simulação).
        producer_id: ID do produtor no Hotmart (não utilizado na simulação).

    Returns:
        Um DataFrame do Pandas com as métricas de performance simuladas.
    """
    # Simulação de dados
    date_range = pd.date_range(start_date, end_date)
    data = []

    for date in date_range:
        # Gera dados diários com uma variação aleatória
        vendas = np.random.randint(2, 15)
        faturamento = vendas * np.random.uniform(47, 297)
        comissao = faturamento * 0.30
        lucro = faturamento - comissao
        
        data.append({
            "date": date,
            "platform": "Hotmart",
            "sales": vendas,
            "revenue": faturamento,
            "commission": comissao,
            "profit": lucro
        })

    return pd.DataFrame(data)


def get_hotmart_products(start_date: datetime, end_date: datetime, token: str, producer_id: str) -> pd.DataFrame:
    """
    Retorna dados detalhados de produtos do Hotmart.
    """
    np.random.seed(321)
    num_products = 8
    
    products_data = []
    for i in range(num_products):
        vendas = np.random.randint(5, 50)
        preco_unitario = np.random.uniform(47, 297)
        faturamento = vendas * preco_unitario
        comissao_hotmart = faturamento * 0.30
        lucro_liquido = faturamento - comissao_hotmart
        
        products_data.append({
            "ID Produto": f"prod_{i+1:03d}",
            "Nome": f"Produto {i+1}",
            "Categoria": np.random.choice(["Cursos", "E-books", "Membressia", "Aplicativos"]),
            "Vendas": vendas,
            "Preço Unitário": preco_unitario,
            "Faturamento": faturamento,
            "Comissão Hotmart": comissao_hotmart,
            "Lucro Líquido": lucro_liquido,
            "Taxa Conversão": np.random.uniform(1, 5)
        })
    
    return pd.DataFrame(products_data)
