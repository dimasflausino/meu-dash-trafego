#!/usr/bin/env python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Analytics Pro", layout="wide", initial_sidebar_state="expanded")

# Tema Dark
st.markdown("""
<style>
    body { background-color: #0B0E14; color: #FFFFFF; }
    .stMetricValue { font-size: 28px; color: #7C3AED; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🛡️ Analytics Pro")
    page = st.radio("Menu", ["🏠 Dashboard", "🔌 Conexões", "🎯 Lead Scoring", "📊 Relatórios"])

# ============ DASHBOARD ============
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
    
    # Gráficos
    dates = pd.date_range(start='2024-01-01', periods=30)
    data = {
        'date': dates,
        'investment': np.random.randint(400, 800, 30),
        'revenue': np.random.randint(1000, 2000, 30)
    }
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['date'], y=df['investment'], name='Investimento', marker_color='#7C3AED'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['revenue'], name='Faturamento', mode='lines+markers', line=dict(color='#10B981', width=3)))
    fig.update_layout(title="Faturamento vs Investimento", hovermode='x unified', height=400, template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela
    st.subheader("📋 Dados Consolidados")
    st.dataframe(df, use_container_width=True)

# ============ CONEXÕES ============
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

# ============ LEAD SCORING ============
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

# ============ RELATÓRIOS ============
elif page == "📊 Relatórios":
    st.title("📊 Relatórios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Meta Ads")
        st.metric("Campanhas", 12)
        st.metric("Gasto", "R$ 5.430")
    
    with col2:
        st.subheader("Google Ads")
        st.metric("Campanhas", 8)
        st.metric("Gasto", "R$ 4.200")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Hotmart")
        st.metric("Vendas", 24)
        st.metric("Faturamento", "R$ 12.500")
    
    with col2:
        st.subheader("Kiwify")
        st.metric("Vendas", 18)
        st.metric("Faturamento", "R$ 8.700")
