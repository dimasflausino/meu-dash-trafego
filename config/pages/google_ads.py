#!/usr/bin/env python
"""
Página de Google Ads

Exibe análise detalhada de campanhas do Google Ads.
Inclui tabelas, gráficos de dispersão e análises de performance.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

from src.services.database_service import get_project_config


def render(project_name: str):
    """Renderiza a página de Google Ads."""
    
    st.title("🔴 Google Ads - Análise Detalhada")

    if not project_name:
        st.warning("⚠️ Selecione um projeto na barra lateral para visualizar os dados.")
        return

    config = get_project_config(project_name)
    if not config:
        st.error(f"❌ Não foi possível carregar a configuração para o projeto '{project_name}'.")
        return

    if not config.Google_Dev:
        st.warning("⚠️ Token do Google Ads não configurado. Vá em '🔌 Conexões' para configurar.")
        return

    # --- FILTROS DE DATA ---
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.date_input(
            "📅 Período",
            (datetime.now() - timedelta(days=7), datetime.now()),
            format="DD/MM/YYYY",
            key="google_date_range"
        )
    
    with col2:
        if st.button("🔄 Atualizar", key="google_refresh"):
            st.cache_data.clear()
            st.rerun()
    
    with col3:
        st.info(f"Projeto: **{project_name}**")

    if len(date_range) != 2:
        st.warning("Por favor, selecione um período de início e fim.")
        return

    start_date, end_date = date_range

    # --- GERAR DADOS SIMULADOS DE CAMPANHAS ---
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
    
    df_campaigns = pd.DataFrame(campaigns_data)

    # --- KPIs ---
    st.subheader("📊 KPIs - Google Ads")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.metric("💰 Gasto Total", f"R$ {df_campaigns['Gasto'].sum():,.2f}")
    
    with kpi_col2:
        st.metric("📈 Faturamento", f"R$ {df_campaigns['Faturamento'].sum():,.2f}")
    
    with kpi_col3:
        st.metric("🎯 Leads", f"{df_campaigns['Leads'].sum():.0f}")
    
    with kpi_col4:
        st.metric("💹 ROI Médio", f"{df_campaigns['ROI'].mean():.2f}%")

    st.divider()

    # --- GRÁFICOS ---
    st.subheader("📉 Análises Visuais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de Dispersão: CPC vs CTR
        fig_scatter = px.scatter(
            df_campaigns,
            x="CTR",
            y="CPC",
            size="Gasto",
            color="ROI",
            hover_data=["Nome", "Tipo", "Gasto", "Leads"],
            title="CPC vs CTR (tamanho = Gasto, cor = ROI)",
            color_continuous_scale="RdYlGn"
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Gráfico de Barras: Top 10 Campanhas por Faturamento
        top_campaigns = df_campaigns.nlargest(10, "Faturamento")
        fig_bars = px.bar(
            top_campaigns,
            x="Faturamento",
            y="Nome",
            orientation="h",
            title="Top 10 Campanhas por Faturamento",
            color="ROI",
            color_continuous_scale="RdYlGn"
        )
        fig_bars.update_layout(height=400)
        st.plotly_chart(fig_bars, use_container_width=True)

    st.divider()

    # --- TABELA DE CAMPANHAS ---
    st.subheader("📋 Campanhas Detalhadas")
    
    # Formatação para exibição
    df_display = df_campaigns.copy()
    df_display["Gasto"] = df_display["Gasto"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["Faturamento"] = df_display["Faturamento"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["CTR"] = df_display["CTR"].apply(lambda x: f"{x:.2f}%")
    df_display["CPC"] = df_display["CPC"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["CPL"] = df_display["CPL"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["ROI"] = df_display["ROI"].apply(lambda x: f"{x:.2f}%")
    
    st.dataframe(df_display, use_container_width=True)

    # --- DOWNLOAD ---
    st.divider()
    csv = df_campaigns.to_csv(index=False)
    st.download_button(
        label="📥 Baixar dados em CSV",
        data=csv,
        file_name=f"google_ads_{start_date}_{end_date}.csv",
        mime="text/csv"
    )

