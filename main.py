import streamlit as st
import pandas as pd
import json

# --- 1. CONFIGURAÇÃO (Deve ser a primeira linha) ---
st.set_page_config(page_title="Analytics Pro SaaS", layout="wide")

# --- 2. ESTILO DARK (PRESERVADO) ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BARRA LATERAL (FIXA - DESENHADA PRIMEIRO) ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    
    # Criamos uma lista de projetos segura para o menu não travar
    if "projetos_memoria" not in st.session_state:
        st.session_state.projetos_memoria = ["Projeto Padrão"]
    
    projeto_ativo = st.selectbox("📁 Projeto Ativo", st.session_state.projetos_memoria + ["+ Novo Projeto"])
    st.divider()
    
    # NAVEGAÇÃO (Nada foi retirado)
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
    st.info(f"Logado: {projeto_ativo}")

# --- 4. CARREGAMENTO DE DADOS (DENTRO DE TRY/EXCEPT) ---
# Se isso aqui falhar, o menu lá em cima já foi desenhado e não some.
def carregar_dados_seguro():
    try:
        # Aqui viria a conexão com o GSheets. 
        # Se der erro, ele cai no 'except' e o app continua vivo.
        return pd.DataFrame() 
    except:
        return pd.DataFrame()

df_db = carregar_dados_seguro()

# --- 5. RENDERIZAÇÃO DAS PÁGINAS ---

if page == "🏠 Dados Consolidados":
    st.title(f"📊 Consolidado: {projeto_ativo}")
    st.write("Visão geral de ROI e Faturamento.")

elif page == "🔵 Meta Ads":
    st.title(f"🔵 Meta Ads - {projeto_ativo}")
    st.write("Dados da API do Facebook.")

elif page == "🔴 Google Ads":
    st.title(f"🔴 Google Ads - {projeto_ativo}")
    st.write("Dados da API do Google.")

elif page == "⚫ TikTok Ads":
    st.title(f"⚫ TikTok Ads - {projeto_ativo}")
    st.write("Dados da API do TikTok.")

elif page == "🟠 Hotmart":
    st.title(f"🟠 Hotmart - {projeto_ativo}")
    st.write("Vendas Hotmart.")

elif page == "🟢 Kiwify":
    st.title(f"🟢 Kiwify - {projeto_ativo}")
    st.write("Vendas Kiwify.")

elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Lead Scoring - {projeto_ativo}")
    st.write("Mapeamento dinâmico de leads.")

elif page == "🌪️ Funil de Perpétuo":
    st.title(f"🌪️ Funil de Perpétuo - {projeto_ativo}")
    st.write("Análise de conversão.")

elif page == "🔌 Conexões":
    st.title("🔌 Configurações de Projetos")
    with st.form("form_seguro"):
        st.subheader(f"⚙️ Configurando: {projeto_ativo}")
        novo_nome = st.text_input("Nome do Projeto")
        
        t1, t2, t3 = st.tabs(["🚀 Captação", "💰 Vendas", "📊 Sheets"])
        with t1: st.write("Tokens de Ads aqui.")
        with t2: st.write("Tokens de Vendas aqui.")
        with t3: st.write("Link do Sheets aqui.")
        
        if st.form_submit_button("💾 Salvar"):
            st.success("Configuração enviada!")
