import streamlit as st
import pandas as pd
import json
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURAÇÃO DA PÁGINA (Sempre a primeira linha) ---
st.set_page_config(page_title="Analytics Pro SaaS", layout="wide")

# --- 2. ESTILO VISUAL DARK (Blindado) ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1f2937; border-radius: 5px; padding: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONEXÃO COM O BANCO DE DADOS ---
def carregar_banco():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Configuracoes", ttl=0)
        return df, conn
    except:
        # Se falhar, cria estrutura vazia para o app não travar
        cols = ["Projeto", "Meta_Token", "Meta_ID", "Google_Dev", "Google_CustID", 
                "TikTok_Token", "TikTok_ID", "Hotmart_ID", "Hotmart_Secret", 
                "Kiwify_Token", "Kiwify_ID", "Sheets_URL", "Col_Tracking", "Regras_JSON"]
        return pd.DataFrame(columns=cols), None

df_db, conn = carregar_banco()

# --- 4. BARRA LATERAL (FIXA E INDEPENDENTE) ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    
    # Lista de projetos segura
    lista_p = []
    if not df_db.empty and "Projeto" in df_db.columns:
        lista_p = df_db["Projeto"].dropna().unique().tolist()
    
    projeto_ativo = st.selectbox("📁 Projeto Ativo", lista_p + ["+ Novo Projeto"])
    st.divider()
    
    # Menu de navegação completo - NUNCA REMOVER
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
    st.info(f"Logado: {projeto
