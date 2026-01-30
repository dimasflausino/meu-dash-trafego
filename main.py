import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Pro - Estilo VK Metrics", layout="wide")

# --- CSS PARA ESTILO DARK PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERAL (NOMES ATUALIZADOS POR VOCÊ) ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    
    page = st.radio("Navegação", [
        "🏠 Dados Consolidados", 
        "🔵 Meta Ads", 
        "🔴 Google Ads", 
        "⚫ TikTok Ads", 
        "🟠 Hotmart", 
        "🟢 Kiwify", 
        "🎯 Lead Scoring",
        "🌪️ Funil de Perpétuo",
        "🔌 Conexões"
    ])
    
    st.divider()
    st.info("Usuário: Administrador")

# --- LÓGICA DAS PÁGINAS ---

if page == "🏠 Dados Consolidados":
    st.title("📊 Dados Consolidados")
    st.write("Resumo geral de performance (VK Metrics Style).")
    # Futuro: KPIs de ROI Global, Faturamento Total e Gasto Total

elif page == "🔵 Meta Ads":
    st.title("🔵 Performance Meta Ads")
    st.write("Métricas de CTR, CPC e Gasto por Campanha vindas da API.")

elif page == "🔴 Google Ads":
    st.title("🔴 Performance Google Ads")
    st.write("Análise de Rede de Pesquisa e Youtube Ads.")

elif page == "⚫ TikTok Ads":
    st.title("⚫ Performance TikTok Ads")
    st.write("Métricas de retenção e conversão de vídeos.")

elif page == "🟠 Hotmart":
    st.title("🟠 Vendas Hotmart")
    st.write("Status de vendas e conversão de checkout.")

elif page == "🟢 Kiwify":
    st.title("🟢 Vendas Kiwify")
    st.write("Faturamento líquido e volume de transações.")

elif page == "🎯 Lead Scoring":
    st.title("🎯 Lead Scoring & Performance de Ads")
    st.subheader("Cruzamento: Meta Ads vs. Leads Qualificados (Sheets)")
    
    # Esta área cruzará o custo do Ad com a qualidade do Lead no Sheets
    st.info("Aqui mostraremos: Nome do Ad | Quantidade | Custo | Leads Qualificados | CPL Real")
    
    # Espaço para o link do Sheets que você usa
    link_sheets = st.text_input("Cole aqui o link CSV da sua planilha de Leads")
    if link_sheets:
        st.write("Analisando qualidade por anúncio...")

elif page == "🌪️ Funil de Perpétuo":
    st.title("🌪️ Funil de Perpétuo")
    st.write("Taxa de conversão de Order Bump, Upsell e Downsell.")

elif page == "🔌 Conexões":
    st.title("🔌 Configurações e Chaves de API")
    st.warning("Insira seus tokens de API abaixo para ativar os dados reais.")
