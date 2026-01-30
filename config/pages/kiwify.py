#!/usr/bin/env python
"""
Página de Kiwify

Exibe análise detalhada de vendas do Kiwify.
Inclui tabelas, gráficos e análises de performance.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

from src.services.database_service import get_project_config


def render(project_name: str):
    """Renderiza a página de Kiwify."""
    
    st.title("🟢 Kiwify - Análise de Vendas")

    if not project_name:
        st.warning("⚠️ Selecione um projeto na barra lateral para visualizar os dados.")
        return

    config = get_project_config(project_name)
    if not config:
        st.error(f"❌ Não foi possível carregar a configuração para o projeto '{project_name}'.")
        return

    if not config.Kiwify_Token:
        st.warning("⚠️ Kiwify não configurado. Vá em '🔌 Conexões' para configurar.")
        return

    # --- FILTROS DE DATA ---
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.date_input(
            "📅 Período",
            (datetime.now() - timedelta(days=7), datetime.now()),
            format="DD/MM/YYYY",
            key="kiwify_date_range"
        )
    
    with col2:
        if st.button("🔄 Atualizar", key="kiwify_refresh"):
            st.cache_data.clear()
            st.rerun()
    
    with col3:
        st.info(f"Projeto: **{project_name}**")

    if len(date_range) != 2:
        st.warning("Por favor, selecione um período de início e fim.")
        return

    start_date, end_date = date_range

    # --- GERAR DADOS SIMULADOS DE PRODUTOS ---
    np.random.seed(321)
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
    
    df_products = pd.DataFrame(products_data)

    # --- KPIs ---
    st.subheader("📊 KPIs - Kiwify")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.metric("🛍️ Total de Vendas", f"{df_products['Vendas'].sum():.0f}")
    
    with kpi_col2:
        st.metric("💵 Faturamento", f"R$ {df_products['Faturamento'].sum():,.2f}")
    
    with kpi_col3:
        st.metric("💰 Lucro Líquido", f"R$ {df_products['Lucro Líquido'].sum():,.2f}")
    
    with kpi_col4:
        st.metric("📈 Ticket Médio", f"R$ {df_products['Preço Unitário'].mean():,.2f}")

    st.divider()

    # --- GRÁFICOS ---
    st.subheader("📉 Análises Visuais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de Barras: Vendas por Produto
        fig_vendas = px.bar(
            df_products.nlargest(6, "Vendas"),
            x="Vendas",
            y="Nome",
            orientation="h",
            title="Vendas por Produto",
            color="Faturamento",
            color_continuous_scale="Plasma"
        )
        fig_vendas.update_layout(height=400)
        st.plotly_chart(fig_vendas, use_container_width=True)
    
    with col2:
        # Gráfico de Pizza: Faturamento por Tipo
        fig_tipo = px.pie(
            df_products.groupby("Tipo")["Faturamento"].sum().reset_index(),
            values="Faturamento",
            names="Tipo",
            title="Faturamento por Tipo de Produto"
        )
        fig_tipo.update_layout(height=400)
        st.plotly_chart(fig_tipo, use_container_width=True)

    st.divider()

    # --- TABELA DE PRODUTOS ---
    st.subheader("📋 Produtos Detalhados")
    
    # Formatação para exibição
    df_display = df_products.copy()
    df_display["Preço Unitário"] = df_display["Preço Unitário"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["Faturamento"] = df_display["Faturamento"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["Comissão Kiwify"] = df_display["Comissão Kiwify"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["Lucro Líquido"] = df_display["Lucro Líquido"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["Taxa Conversão"] = df_display["Taxa Conversão"].apply(lambda x: f"{x:.2f}%")
    
    st.dataframe(df_display, use_container_width=True)

    # --- DOWNLOAD ---
    st.divider()
    csv = df_products.to_csv(index=False)
    st.download_button(
        label="📥 Baixar dados em CSV",
        data=csv,
        file_name=f"kiwify_{start_date}_{end_date}.csv",
        mime="text/csv"
    )

