#!/usr/bin/env python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Analytics Pro", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    body { background-color: #0B0E14; color: #FFFFFF; }
    .stMetricValue { font-size: 28px; color: #7C3AED; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🛡️ Analytics Pro")
    page = st.radio("Menu", [
        "🏠 Dashboard", 
        "🔵 Meta Ads",
        "🔴 Google Ads",
        "⚫ TikTok Ads",
        "🟠 Hotmart",
        "🟢 Kiwify",
        "🔌 Conexões", 
        "🎯 Lead Scoring"
    ])

def gerar_dados_meta(dias=30):
    dates = pd.date_range(start=datetime.now() - timedelta(days=dias), periods=dias)
    return pd.DataFrame({
        'data': dates,
        'impressoes': np.random.randint(10000, 50000, dias),
        'cliques': np.random.randint(500, 2000, dias),
        'conversoes': np.random.randint(50, 200, dias),
        'gasto': np.random.uniform(500, 2000, dias),
        'faturamento': np.random.uniform(1500, 5000, dias),
    })

def gerar_dados_google(dias=30):
    dates = pd.date_range(start=datetime.now() - timedelta(dias=dias), periods=dias)
    return pd.DataFrame({
        'data': dates,
        'impressoes': np.random.randint(8000, 40000, dias),
        'cliques': np.random.randint(400, 1500, dias),
        'conversoes': np.random.randint(40, 150, dias),
        'gasto': np.random.uniform(400, 1800, dias),
        'faturamento': np.random.uniform(1200, 4500, dias),
    })

def gerar_dados_tiktok(dias=30):
    dates = pd.date_range(start=datetime.now() - timedelta(dias=dias), periods=dias)
    return pd.DataFrame({
        'data': dates,
        'impressoes': np.random.randint(15000, 60000, dias),
        'cliques': np.random.randint(800, 3000, dias),
        'conversoes': np.random.randint(60, 250, dias),
        'gasto': np.random.uniform(300, 1500, dias),
        'faturamento': np.random.uniform(1000, 4000, dias),
    })

def gerar_anuncios_meta():
    return pd.DataFrame({
        'ID': ['ad_001', 'ad_002', 'ad_003', 'ad_004', 'ad_005'],
        'Nome': ['Anúncio 1', 'Anúncio 2', 'Anúncio 3', 'Anúncio 4', 'Anúncio 5'],
        'Status': ['Ativo', 'Ativo', 'Pausado', 'Ativo', 'Ativo'],
        'Impressões': [45230, 38920, 12450, 56780, 34560],
        'Cliques': [1230, 980, 320, 1890, 890],
        'CTR': [2.72, 2.52, 2.57, 3.33, 2.57],
        'Gasto': [1250.50, 980.30, 450.20, 1890.75, 750.40],
        'Conversões': [45, 38, 12, 67, 34],
        'CPL': [27.79, 25.80, 37.52, 28.22, 22.07],
        'ROI': [185, 210, 95, 245, 190]
    })

def gerar_campanhas_google():
    return pd.DataFrame({
        'ID': ['camp_001', 'camp_002', 'camp_003', 'camp_004'],
        'Nome': ['Campanha Search 1', 'Campanha Display 1', 'Campanha Shopping', 'Campanha Video'],
        'Status': ['Ativo', 'Ativo', 'Pausado', 'Ativo'],
        'Impressões': [32100, 28900, 15600, 42300],
        'Cliques': [890, 650, 380, 1200],
        'CTR': [2.77, 2.25, 2.44, 2.84],
        'Gasto': [980.50, 750.20, 420.30, 1320.80],
        'Conversões': [32, 28, 15, 42],
        'CPC': [1.10, 1.15, 1.11, 1.10],
        'ROI': [195, 215, 105, 235]
    })

def gerar_campanhas_tiktok():
    return pd.DataFrame({
        'ID': ['tt_001', 'tt_002', 'tt_003', 'tt_004'],
        'Nome': ['Campanha TT 1', 'Campanha TT 2', 'Campanha TT 3', 'Campanha TT 4'],
        'Status': ['Ativo', 'Ativo', 'Ativo', 'Pausado'],
        'Impressões': [65400, 52300, 48900, 31200],
        'Cliques': [2100, 1680, 1560, 890],
        'CTR': [3.21, 3.21, 3.19, 2.85],
        'Gasto': [850.30, 720.50, 680.20, 450.10],
        'Conversões': [65, 52, 48, 31],
        'CPC': [0.40, 0.43, 0.44, 0.51],
        'ROI': [265, 245, 235, 180]
    })

if page == "🏠 Dashboard":
    st.title("📊 Dashboard Consolidado")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Investimento", "R$ 15.430", "+5%")
    with col2:
        st.metric("📊 Faturamento", "R$ 45.200", "+12%")
    with col3:
        st.metric("💸 Lucro", "R$ 29.770", "+8%")
    with col4:
        st.metric("💹 ROI", "193%", "+15%")
    
    st.divider()
    df_meta = gerar_dados_meta()
    df_google = gerar_dados_google()
    df_tiktok = gerar_dados_tiktok()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_meta['data'], y=df_meta['gasto'], name='Meta Ads', marker_color='#1877F2'))
    fig.add_trace(go.Bar(x=df_google['data'], y=df_google['gasto'], name='Google Ads', marker_color='#EA4335'))
    fig.add_trace(go.Bar(x=df_tiktok['data'], y=df_tiktok['gasto'], name='TikTok Ads', marker_color='#000000'))
    fig.update_layout(title="Gasto por Plataforma", barmode='group', height=400, template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

elif page == "🔵 Meta Ads":
    st.title("🔵 Meta Ads - Análise Detalhada")
    df_meta = gerar_dados_meta()
    df_anuncios = gerar_anuncios_meta()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Gasto Total", f"R$ {df_meta['gasto'].sum():.2f}")
    with col2:
        st.metric("📊 Faturamento", f"R$ {df_meta['faturamento'].sum():.2f}")
    with col3:
        st.metric("✅ Conversões", f"{df_meta['conversoes'].sum():.0f}")
    with col4:
        st.metric("💹 ROI", f"{((df_meta['faturamento'].sum() / df_meta['gasto'].sum() - 1) * 100):.1f}%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df_meta, x='data', y=['gasto', 'faturamento'], title='Gasto vs Faturamento', markers=True)
        fig.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.scatter(df_anuncios, x='CTR', y='ROI', size='Gasto', hover_name='Nome', title='CTR vs ROI')
        fig2.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    st.subheader("📋 Todos os Anúncios")
    st.dataframe(df_anuncios, use_container_width=True)

elif page == "🔴 Google Ads":
    st.title("🔴 Google Ads - Análise Detalhada")
    df_google = gerar_dados_google()
    df_campanhas = gerar_campanhas_google()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Gasto Total", f"R$ {df_google['gasto'].sum():.2f}")
    with col2:
        st.metric("📊 Faturamento", f"R$ {df_google['faturamento'].sum():.2f}")
    with col3:
        st.metric("✅ Conversões", f"{df_google['conversoes'].sum():.0f}")
    with col4:
        st.metric("💹 ROI", f"{((df_google['faturamento'].sum() / df_google['gasto'].sum() - 1) * 100):.1f}%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df_google, x='data', y=['gasto', 'faturamento'], title='Gasto vs Faturamento', markers=True)
        fig.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.scatter(df_campanhas, x='CTR', y='ROI', size='Gasto', hover_name='Nome', title='CTR vs ROI')
        fig2.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    st.subheader("📋 Todas as Campanhas")
    st.dataframe(df_campanhas, use_container_width=True)

elif page == "⚫ TikTok Ads":
    st.title("⚫ TikTok Ads - Análise Detalhada")
    df_tiktok = gerar_dados_tiktok()
    df_campanhas_tt = gerar_campanhas_tiktok()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Gasto Total", f"R$ {df_tiktok['gasto'].sum():.2f}")
    with col2:
        st.metric("📊 Faturamento", f"R$ {df_tiktok['faturamento'].sum():.2f}")
    with col3:
        st.metric("✅ Conversões", f"{df_tiktok['conversoes'].sum():.0f}")
    with col4:
        st.metric("💹 ROI", f"{((df_tiktok['faturamento'].sum() / df_tiktok['gasto'].sum() - 1) * 100):.1f}%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df_tiktok, x='data', y=['gasto', 'faturamento'], title='Gasto vs Faturamento', markers=True)
        fig.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.scatter(df_campanhas_tt, x='CTR', y='ROI', size='Gasto', hover_name='Nome', title='CTR vs ROI')
        fig2.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    st.subheader("📋 Todas as Campanhas")
    st.dataframe(df_campanhas_tt, use_container_width=True)

elif page == "🟠 Hotmart":
    st.title("🟠 Hotmart - Vendas")
    df_hotmart = pd.DataFrame({
        'data': pd.date_range(start=datetime.now() - timedelta(days=30), periods=30),
        'vendas': np.random.randint(5, 20, 30),
        'faturamento': np.random.uniform(500, 2000, 30),
    })
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Vendas Total", f"{df_hotmart['vendas'].sum():.0f}")
    with col2:
        st.metric("💰 Faturamento", f"R$ {df_hotmart['faturamento'].sum():.2f}")
    with col3:
        st.metric("🎯 Ticket Médio", f"R$ {df_hotmart['faturamento'].sum() / df_hotmart['vendas'].sum():.2f}")
    
    st.divider()
    fig = px.line(df_hotmart, x='data', y='faturamento', title='Faturamento Hotmart', markers=True)
    fig.update_layout(height=400, template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

elif page == "🟢 Kiwify":
    st.title("🟢 Kiwify - Vendas")
    df_kiwify = pd.DataFrame({
        'data': pd.date_range(start=datetime.now() - timedelta(days=30), periods=30),
        'vendas': np.random.randint(3, 15, 30),
        'faturamento': np.random.uniform(300, 1500, 30),
    })
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Vendas Total", f"{df_kiwify['vendas'].sum():.0f}")
    with col2:
        st.metric("💰 Faturamento", f"R$ {df_kiwify['faturamento'].sum():.2f}")
    with col3:
        st.metric("🎯 Ticket Médio", f"R$ {df_kiwify['faturamento'].sum() / df_kiwify['vendas'].sum():.2f}")
    
    st.divider()
    fig = px.line(df_kiwify, x='data', y='faturamento', title='Faturamento Kiwify', markers=True)
    fig.update_layout(height=400, template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

elif page == "🔌 Conexões":
    st.title("🔌 Configurar Conexões")
    with st.form("conexoes_form"):
        st.subheader("Meta Ads")
        meta_token = st.text_input("Token Meta", type="password")
        meta_id = st.text_input("ID da Conta")
        
        st.divider()
        st.subheader("Google Ads")
        google_token = st.text_input("Token Google", type="password")
        google_id = st.text_input("ID do Cliente")
        
        st.divider()
        st.subheader("TikTok Ads")
        tiktok_token = st.text_input("Token TikTok", type="password")
        tiktok_id = st.text_input("ID da Conta TikTok")
        
        st.divider()
        st.subheader("Hotmart")
        hotmart_token = st.text_input("Token Hotmart", type="password")
        
        st.divider()
        st.subheader("Kiwify")
        kiwify_token = st.text_input("Token Kiwify", type="password")
        
        if st.form_submit_button("💾 Salvar Configurações"):
            st.success("✅ Configurações salvas com sucesso!")

elif page == "🎯 Lead Scoring":
    st.title("🎯 Lead Scoring Dinâmico")
    tab1, tab2 = st.tabs(["Criar Regras", "Pontuar Leads"])
    
    with tab1:
        st.subheader("Criar Regras de Pontuação")
        with st.form("lead_scoring_form"):
            regra_nome = st.text_input("Nome da Regra")
            regra_coluna = st.selectbox("Coluna", ["Email", "Telefone", "Origem", "Status"])
            regra_valor = st.text_input("Valor")
            regra_pontos = st.number_input("Pontos", min_value=0, max_value=100)
            
            if st.form_submit_button("➕ Adicionar Regra"):
                st.success(f"✅ Regra '{regra_nome}' adicionada!")
    
    with tab2:
        st.subheader("Pontuar Leads")
        uploaded_file = st.file_uploader("Enviar arquivo CSV", type="csv")
        if uploaded_file:
            df_leads = pd.read_csv(uploaded_file)
            st.dataframe(df_leads)
            if st.button("🎯 Pontuar Leads"):
                st.success("✅ Leads pontuados!")
