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

# --- MENU LATERAL (TODOS OS SEUS MENUS ESTÃO AQUI) ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    
    # Lista de navegação completa conforme seu pedido
    page = st.radio("Navegação", [
        "🏠 Visão Geral", 
        "🔵 Meta Ads (Facebook)", 
        "🔴 Google Ads", 
        "⚫ TikTok Ads", 
        "🟠 Hotmart", 
        "🟢 Kiwify", 
        "🎯 Qualidade por Ad (Lead Scoring)",
        "🌪️ Funil de Perpétuo",
        "🔌 Conexões"
    ])
    
    st.divider()
    st.info("Usuário: Administrador")

# --- LÓGICA DAS PÁGINAS (CONSTRUINDO O CONTEÚDO) ---

if page == "🏠 Visão Geral":
    st.title("Consolidado de Performance")
    st.write("Resumo geral de todas as suas fontes de tráfego e vendas.")
    # Aqui colocaremos os cartões de ROAS Global e Lucro Total

elif page == "🔵 Meta Ads (Facebook)":
    st.title("Performance Meta Ads")
    st.write("Métricas de CTR, CPC e Gasto por Campanha.")

elif page == "🔴 Google Ads":
    st.title("Performance Google Ads")
    st.write("Análise de Rede de Pesquisa e Youtube Ads.")

elif page == "⚫ TikTok Ads":
    st.title("Performance TikTok Ads")
    st.write("Métricas de retenção e conversão de vídeos.")

elif page == "🟠 Hotmart":
    st.title("Vendas Hotmart")
    st.write("Acompanhamento de vendas, boletos gerados e cartões aprovados.")

elif page == "🟢 Kiwify":
    st.title("Vendas Kiwify")
    st.write("Faturamento líquido e volume de transações.")

elif page == "🎯 Qualidade por Ad (Lead Scoring)":
    st.title("Cruzamento: Meta Ads vs. Leads Qualificados")
    st.subheader("Onde o tráfego encontra o lucro real")
    # Aqui entra o código de cruzamento (UTM do Sheets + Custo do Meta)
    st.write("Esta página mostra qual anúncio específico está trazendo o lead que você quer.")

elif page == "🌪️ Funil de Perpétuo":
    st.title("Análise de Checkout (Upsell/Order Bump)")
    st.write("Cálculo de taxa de conversão entre produtos separados.")

elif page == "🔌 Conexões":
    st.title("Configurações e Chaves de API")
    st.warning("Insira seus tokens aqui para ativar os menus acima.")
