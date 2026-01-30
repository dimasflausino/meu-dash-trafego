#!/usr/bin/env python
"""
Página de Funil de Perpétuo

Exibe análise do funil de vendas e sequências de automação.
Inclui gráficos de funil, conversão e análises de performance.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

from src.services.database_service import get_project_config


def render(project_name: str):
    """Renderiza a página de Funil de Perpétuo."""
    
    st.title("🌪️ Funil de Perpétuo - Análise de Conversão")

    if not project_name:
        st.warning("⚠️ Selecione um projeto na barra lateral para visualizar os dados.")
        return

    config = get_project_config(project_name)
    if not config:
        st.error(f"❌ Não foi possível carregar a configuração para o projeto '{project_name}'.")
        return

    # --- FILTROS DE DATA ---
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.date_input(
            "📅 Período",
            (datetime.now() - timedelta(days=30), datetime.now()),
            format="DD/MM/YYYY",
            key="funil_date_range"
        )
    
    with col2:
        if st.button("🔄 Atualizar", key="funil_refresh"):
            st.cache_data.clear()
            st.rerun()
    
    with col3:
        st.info(f"Projeto: **{project_name}**")

    if len(date_range) != 2:
        st.warning("Por favor, selecione um período de início e fim.")
        return

    start_date, end_date = date_range

    # --- DADOS DO FUNIL ---
    funil_data = {
        "Etapa": ["Visitantes", "Leads", "Clientes", "Clientes Recorrentes"],
        "Quantidade": [10000, 850, 127, 32],
        "Conversão": [100, 8.5, 14.9, 25.2]
    }
    
    df_funil = pd.DataFrame(funil_data)
    
    # Calcular taxa de conversão entre etapas
    df_funil["Taxa Anterior"] = [100.0] + [
        (df_funil.loc[i, "Quantidade"] / df_funil.loc[i-1, "Quantidade"] * 100) 
        for i in range(1, len(df_funil))
    ]

    # --- KPIs ---
    st.subheader("📊 KPIs - Funil de Perpétuo")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.metric("👥 Visitantes", f"{df_funil.iloc[0]['Quantidade']:,.0f}")
    
    with kpi_col2:
        st.metric("📧 Leads", f"{df_funil.iloc[1]['Quantidade']:,.0f}")
    
    with kpi_col3:
        st.metric("🛒 Clientes", f"{df_funil.iloc[2]['Quantidade']:,.0f}")
    
    with kpi_col4:
        taxa_conversao = (df_funil.iloc[2]['Quantidade'] / df_funil.iloc[0]['Quantidade'] * 100)
        st.metric("💹 Taxa Conversão", f"{taxa_conversao:.2f}%")

    st.divider()

    # --- GRÁFICOS ---
    st.subheader("📉 Análises Visuais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de Funil
        fig_funil = go.Figure(go.Funnel(
            y=df_funil["Etapa"],
            x=df_funil["Quantidade"],
            textposition="inside",
            textinfo="value+percent previous",
            marker=dict(color=["#7C3AED", "#6D28D9", "#10B981", "#F59E0B"])
        ))
        
        fig_funil.update_layout(
            title="Funil de Conversão",
            height=400
        )
        st.plotly_chart(fig_funil, use_container_width=True)
    
    with col2:
        # Gráfico de Taxa de Conversão
        fig_taxa = px.bar(
            df_funil,
            x="Etapa",
            y="Taxa Anterior",
            title="Taxa de Conversão entre Etapas (%)",
            color="Taxa Anterior",
            color_continuous_scale="RdYlGn"
        )
        fig_taxa.update_layout(height=400)
        st.plotly_chart(fig_taxa, use_container_width=True)

    st.divider()

    # --- ANÁLISE DE SEQUÊNCIAS ---
    st.subheader("📧 Sequências de Automação")
    
    sequences_data = {
        "Sequência": ["Bem-vindo", "Apresentação", "Oferta", "Urgência", "Recapitulação"],
        "Emails Enviados": [10000, 8500, 7225, 6141, 5220],
        "Taxa Abertura": [35.2, 28.5, 22.1, 18.9, 15.3],
        "Taxa Clique": [8.5, 6.2, 4.8, 3.9, 2.1],
        "Conversões": [127, 95, 68, 42, 18]
    }
    
    df_sequences = pd.DataFrame(sequences_data)

    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de Linha: Taxa de Abertura
        fig_abertura = px.line(
            df_sequences,
            x="Sequência",
            y="Taxa Abertura",
            markers=True,
            title="Taxa de Abertura por Sequência (%)",
            line_shape="linear"
        )
        fig_abertura.update_layout(height=400)
        st.plotly_chart(fig_abertura, use_container_width=True)
    
    with col2:
        # Gráfico de Linha: Conversões
        fig_conversoes = px.line(
            df_sequences,
            x="Sequência",
            y="Conversões",
            markers=True,
            title="Conversões por Sequência",
            line_shape="linear"
        )
        fig_conversoes.update_layout(height=400)
        st.plotly_chart(fig_conversoes, use_container_width=True)

    st.divider()

    # --- TABELA DE SEQUÊNCIAS ---
    st.subheader("📋 Detalhes das Sequências")
    
    # Formatação para exibição
    df_seq_display = df_sequences.copy()
    df_seq_display["Taxa Abertura"] = df_seq_display["Taxa Abertura"].apply(lambda x: f"{x:.2f}%")
    df_seq_display["Taxa Clique"] = df_seq_display["Taxa Clique"].apply(lambda x: f"{x:.2f}%")
    
    st.dataframe(df_seq_display, use_container_width=True)

    # --- DOWNLOAD ---
    st.divider()
    csv = df_sequences.to_csv(index=False)
    st.download_button(
        label="📥 Baixar dados em CSV",
        data=csv,
        file_name=f"funil_perpetuo_{start_date}_{end_date}.csv",
        mime="text/csv"
    )

