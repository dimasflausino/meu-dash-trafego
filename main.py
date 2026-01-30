import streamlit as st
import pandas as pd
import json
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Pro SaaS", layout="wide")

# --- CSS DARK PREMIUM (MANTIDO) ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1f2937; border-radius: 5px; padding: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO BANCO DE DADOS (MEMÓRIA) ---
if "banco_projetos" not in st.session_state:
    st.session_state["banco_projetos"] = {
        "Projeto Padrão": {
            "Meta_Token": "", "Kiwify_Token": "", "Sheets_URL": "",
            "Col_Tracking": "utm_content", "Regras_JSON": "[]"
        }
    }

# --- FUNÇÃO DE CÁLCULO DE SCORE (AGNOSTICA PARA SAAS) ---
def aplicar_scoring(df, regras_json):
    df['Score_Total'] = 0
    try:
        regras = json.loads(regras_json) if isinstance(regras_json, str) else regras_json
        for r in regras:
            col, val, pts = r['coluna'], r['valor'], r['pontos']
            if col in df.columns:
                df.loc[df[col].astype(str).str.contains(val, case=False, na=False), 'Score_Total'] += pts
    except:
        pass
    return df

# --- MENU LATERAL COMPLETO ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    
    lista_p = list(st.session_state["banco_projetos"].keys())
    projeto_ativo = st.selectbox("📁 Projeto Ativo", lista_p + ["+ Novo Projeto"])
    st.divider()
    
    if projeto_ativo == "+ Novo Projeto":
        page = "🔌 Conexões"
    else:
        page = st.radio("Navegação", [
            "🏠 Dados Consolidados", "🔵 Meta Ads", "🔴 Google Ads", 
            "⚫ TikTok Ads", "🟠 Hotmart", "🟢 Kiwify", 
            "🎯 Lead Scoring", "🌪️ Funil de Perpétuo", "🔌 Conexões"
        ])

# --- LÓGICA DAS PÁGINAS ---

if page == "🔌 Conexões":
    st.title("🔌 Configurações de Projetos e APIs")
    
    with st.form("form_master"):
        st.subheader(f"⚙️ Editando: {projeto_ativo}")
        nome_p = st.text_input("Nome do Projeto", value="" if projeto_ativo == "+ Novo Projeto" else projeto_ativo)
        
        tab_t, tab_v, tab_d = st.tabs(["🚀 Plataforma de Captação", "💰 Plataforma de Vendas", "📊 Sheets"])
        
        with tab_t:
            st.write("**Meta Ads**"); m_t = st.text_input("Access Token", type="password")
            st.write("**Google Ads**"); g_d = st.text_input("Developer Token")
            st.write("**TikTok Ads**"); t_t = st.text_input("Access Token TikTok", type="password")
        
        with tab_v:
            st.write("**Hotmart**"); h_i = st.text_input("Client ID")
            st.write("**Kiwify**"); k_t = st.text_input("API Key", type="password")
            
        with
