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

# ============ FUNÇÕES AUXILIARES ============
def gerar_dados_meta(dias=30):
    dates = pd.date_range(start=datetime.now() - timedelta(days=dias), periods=dias)
    return pd.DataFrame({
        'data': dates,
        'campanhas': np.random.randint(5, 15, dias),
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
        'campanhas': np.random.randint(3, 10, dias),
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
        'campanhas': np.random.randint(2, 8, dias),
        'impressoes': np.random.randint(15000, 60000, dias),
        'cliques': np.random.randint(800, 3000, dias),
        'conversoes': np.random.randint(60, 250, dias),
        'gasto': np.random.uniform(300, 1500, dias),
        'faturamento': np.random.uniform(1000, 4000, dias),
    })

def gerar_anuncios_meta():
    return pd.DataFrame({
        'ID': ['ad_001', 'ad_002', 'ad_003', 'ad_004', 'ad_005', 'ad_006', 'ad_007', 'ad_008'],
        'Nome': ['Anúncio 1', 'Anúncio 2', 'Anúncio 3', 'Anúncio 4', 'Anúncio 5', 'Anúncio 6', 'Anúncio 7', 'Anúncio 8'],
        'Status': ['Ativo', 'Ativo', 'Pausado', 'Ativo', 'Ativo', 'Ativo', 'Pausado', 'Ativo'],
        'Impressões': [45230, 38920, 12450, 56780, 34560, 42100, 18900, 51200],
        'Cliques': [1230, 980, 320, 1890, 890, 1150, 450, 1380],
        'CTR': [2.72, 2.52, 2.57, 3.33, 2.57, 2.73, 2.38, 2.69],
        'Gasto': [1250.50, 980.30, 450.20, 1890.75, 750.40, 1100.20, 520.80, 1450.60],
        'Conversões': [45, 38, 12, 67, 34, 42, 18, 55],
        'CPL': [27.79, 25.80, 37.52, 28.22, 22.07, 26.19, 28.93, 26.38],
        'ROI': [185, 210, 95, 245, 190, 215, 110, 230]
    })

def gerar_campanhas_google():
    return pd.DataFrame({
        'ID': ['camp_001', 'camp_002', 'camp_003', 'camp_004', 'camp_005', 'camp_006'],
        'Nome': ['Campanha Search 1', 'Campanha Display 1', 'Campanha Shopping', 'Campanha Video', 'Campanha Search 2', 'Campanha Display 2'],
        'Status': ['Ativo', 'Ativo', 'Pausado', 'Ativo', 'Ativo', 'Ativo'],
        'Impressões': [32100, 28900, 15600, 42300, 38500, 25600],
        'Cliques': [890, 650, 380, 1200, 1050, 720],
        'CTR': [2.77, 2.25, 2.44, 2.84, 2.73, 2.81],
        'Gasto': [980.50, 750.20, 420.30, 1320.80, 1150.40, 890.60],
        'Conversões': [32, 28, 15, 42, 38, 26],
        'CPC': [1.10, 1.15, 1.11, 1.10, 1.10, 1.24],
        'ROI': [195, 215, 105, 235, 220, 185]
    })

def gerar_campanhas_tiktok():
    return pd.DataFrame({
        'ID': ['tt_001', 'tt_002', 'tt_003', 'tt_004', 'tt_005', 'tt_006'],
        'Nome': ['Campanha TT 1', 'Campanha TT 2', 'Campanha TT 3', 'Campanha TT 4', 'Campanha TT 5', 'Campanha TT 6'],
        'Status': ['Ativo', 'Ativo', 'Ativo', 'Pausado', 'Ativo', 'Ativo'],
        'Impressões': [65400, 52300, 48900, 31200, 58700, 44200],
        'Cliques': [2100, 1680, 1560, 890, 1920, 1450],
        'CTR': [3.21, 3.21, 3.19, 2.85, 3.27, 3.28],
        'Gasto': [850.30, 720.50, 680.20, 450.10, 780.90, 620.40],
        'Conversões': [65, 52, 48, 31, 58, 44],
        'CPC': [0.40, 0.43, 0.44, 0.51, 0.41, 0.43],
        'ROI': [265, 245, 235, 180, 255, 240]
    })

def gerar_produtos_hotmart():
    return pd.DataFrame({
        'ID': ['hot_001', 'hot_002', 'hot_003', 'hot_004', 'hot_005'],
        'Nome': ['Produto 1', 'Produto 2', 'Produto 3', 'Produto 4', 'Produto 5'],
        'Categoria': ['Infoproduto', 'Curso', 'Infoproduto', 'Assinatura', 'Curso'],
        'Vendas': [45, 38, 52, 28, 35],
        'Preço Unitário': [97.00, 127.00, 67.00, 47.00, 157.00],
        'Faturamento': [4365.00, 4826.00, 3484.00, 1316.00, 5495.00],
        'Comissão': [654.75, 723.90, 522.60, 197.40, 824.25],
        'Lucro Líquido': [3710.25, 4102.10, 2961.40, 1118.60, 4670.75],
        'Taxa Conversão': [2.3, 1.8, 2.8, 1.5, 2.1]
    })

def gerar_produtos_kiwify():
    return pd.DataFrame({
        'ID': ['kiwi_001', 'kiwi_002', 'kiwi_003', 'kiwi_004'],
        'Nome': ['Produto Kiwify 1', 'Produto Kiwify 2', 'Produto Kiwify 3', 'Produto Kiwify 4'],
        'Tipo': ['Infoproduto', 'Assinatura', 'Serviço', 'Infoproduto'],
        'Vendas': [32, 28, 18, 25],
        'Preço Unitário': [87.00, 37.00, 157.00, 77.00],
        'Faturamento': [2784.00, 1036.00, 2826.00, 1925.00],
        'Comissão': [417.60, 155.40, 423.90, 288.75],
        'Lucro Líquido': [2366.40, 880.60, 2402.10, 1636.25],
        'Taxa Conversão': [1.9, 1.2, 2.5, 1.7]
    })

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
    
    df_meta = gerar_dados_meta()
    df_google = gerar_dados_google()
    df_tiktok = gerar_dados_tiktok()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_meta['data'], y=df_meta['gasto'], name='Meta Ads', marker_color='#1877F2'))
    fig.add_trace(go.Bar(x=df_google['data'], y=df_google['gasto'], name='Google Ads', marker_color='#EA4335'))
    fig.add_trace(go.Bar(x=df_tiktok['data'], y=df_tiktok['gasto'], name='TikTok Ads', marker_color='#000000'))
    fig.update_layout(title="Gasto por Plataforma", barmode='group', height=400, template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🔵 Meta Ads")
        st.metric("Gasto Total", f"R$ {df_meta['gasto'].sum():.2f}")
        st.metric("Faturamento", f"R$ {df_meta['faturamento'].sum():.2f}")
        st.metric("ROI", f"{((df_meta['faturamento'].sum() / df_meta['gasto'].sum() - 1) * 100):.1f}%")
    
    with col2:
        st.subheading("🔴 Google Ads")
        st.metric("Gasto Total", f"R$ {df_google['gasto'].sum():.2f}")
        st.metric("Faturamento", f"R$ {df_google['faturamento'].sum():.2f}")
        st.metric("ROI", f"{((df_google['faturamento'].sum() / df_google['gasto'].sum() - 1) * 100):.1f}%")
    
    with col3:
        st.subheading("⚫ TikTok Ads")
        st.metric("Gasto Total", f"R$ {df_tiktok['gasto'].sum():.2f}")
        st.metric("Faturamento", f"R$ {df_tiktok['faturamento'].sum():.2f}")
        st.metric("ROI", f"{((df_tiktok['faturamento'].sum() / df_tiktok['gasto'].sum() - 1) * 100):.1f}%")

# ============ META ADS ============
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
        fig2 = px.scatter(df_anuncios, x='CTR', y='ROI', size='Gasto', hover_name='Nome', title='CTR vs ROI', color='Status')
        fig2.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig3 = px.bar(df_anuncios.nlargest(5, 'Faturamento'), x='Nome', y='Faturamento', title='Top 5 Anúncios por Faturamento', color='ROI')
        fig3.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        fig4 = px.bar(df_anuncios.nlargest(5, 'Conversoes'), x='Nome', y='Conversoes', title='Top 5 Anúncios por Conversões')
        fig4.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig4, use_container_width=True)
    
    st.divider()
    
    st.subheader("📋 Todos os Anúncios")
    st.dataframe(df_anuncios, use_container_width=True)
    
    csv = df_anuncios.to_csv(index=False)
    st.download_button(label="📥 Baixar CSV", data=csv, file_name="meta_ads.csv", mime="text/csv")

# ============ GOOGLE ADS ============
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
        fig2 = px.scatter(df_campanhas, x='CTR', y='ROI', size='Gasto', hover_name='Nome', title='CTR vs ROI', color='Status')
        fig2.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig3 = px.bar(df_campanhas.nlargest(5, 'Faturamento'), x='Nome', y='Faturamento', title='Top 5 Campanhas por Faturamento', color='ROI')
        fig3.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        fig4 = px.bar(df_campanhas.nlargest(5, 'Conversoes'), x='Nome', y='Conversoes', title='Top 5 Campanhas por Conversões')
        fig4.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig4, use_container_width=True)
    
    st.divider()
    
    st.subheader("📋 Todas as Campanhas")
    st.dataframe(df_campanhas, use_container_width=True)
    
    csv = df_campanhas.to_csv(index=False)
    st.download_button(label="📥 Baixar CSV", data=csv, file_name="google_ads.csv", mime="text/csv")

# ============ TIKTOK ADS ============
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
        fig2 = px.scatter(df_campanhas_tt, x='CTR', y='ROI', size='Gasto', hover_name='Nome', title='CTR vs ROI', color='Status')
        fig2.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig3 = px.bar(df_campanhas_tt.nlargest(5, 'Faturamento'), x='Nome', y='Faturamento', title='Top 5 Campanhas por Faturamento', color='ROI')
        fig3.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        fig4 = px.bar(df_campanhas_tt.nlargest(5, 'Conversoes'), x='Nome', y='Conversoes', title='Top 5 Campanhas por Conversões')
        fig4.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig4, use_container_width=True)
    
    st.divider()
    
    st.subheader("📋 Todas as Campanhas")
    st.dataframe(df_campanhas_tt, use_container_width=True)
    
    csv = df_campanhas_tt.to_csv(index=False)
    st.download_button(label="📥 Baixar CSV", data=csv, file_name="tiktok_ads.csv", mime="text/csv")

# ============ HOTMART ============
elif page == "🟠 Hotmart":
    st.title("🟠 Hotmart - Vendas")
    
    df_hotmart = pd.DataFrame({
        'data': pd.date_range(start=datetime.now() - timedelta(days=30), periods=30),
        'vendas': np.random.randint(5, 20, 30),
        'faturamento': np.random.uniform(500, 2000, 30),
    })
    
    df_produtos = gerar_produtos_hotmart()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Vendas Total", f"{df_hotmart['vendas'].sum():.0f}")
    with col2:
        st.metric("💰 Faturamento", f"R$ {df_hotmart['faturamento'].sum():.2f}")
    with col3:
        st.metric("🎯 Ticket Médio", f"R$ {df_hotmart['faturamento'].sum() / df_hotmart['vendas'].sum():.2f}")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(df_hotmart, x='data', y='faturamento', title='Faturamento Hotmart', markers=True)
        fig.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig2 = px.bar(df_produtos.nlargest(5, 'Faturamento'), x='Nome', y='Faturamento', title='Top 5 Produtos por Faturamento', color='Categoria')
        fig2.update_layout(height=400, template='plotly_dark')
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    st.subheader("📋 Produtos Hotmart")
    st.dataframe(df_produtos, use_container_width=True)
    
    csv = df_produtos.to_csv(index=False)
    st.download_button(label="📥 Baixar CSV", data=csv, file_name="hotmart.csv", mime="text/csv")

# ============ KIWIFY ============
elif page == "🟢 Kiwify":
    st.title("🟢 Kiwify - Vendas")
    
    df_kiwify = pd.DataFrame({
        'data': pd.date_range(start=datetime.now() - timedelta(days=30), periods=30),
        'vendas': np.random.randint(3, 15, 30),
        'faturamento': np.random.uniform(300, 1500, 30),
    })
    
    df_produtos = gerar_produtos_kiwify()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Vendas Total", f"{df_kiwify['vendas'].sum():.0f}")
    with col2:
  
(Content truncated due to size limit. Use line ranges to read remaining content)
