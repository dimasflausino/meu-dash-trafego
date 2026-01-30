import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Pro - Multi-Projeto", layout="wide")

# --- CSS PARA ESTILO DARK PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERAL ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    
    # NOVO: Seleção de Projeto
    projeto_ativo = st.selectbox("📁 Projeto Ativo", ["Projeto Alpha", "Projeto Beta", "Novo Projeto..."])
    st.divider()
    
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
    st.info(f"Projeto: {projeto_ativo}")

# --- LÓGICA DE DADOS POR PROJETO ---
# Aqui o sistema entende qual API usar baseado no projeto selecionado
def carregar_configuracoes(nome_projeto):
    # Futuramente, isso buscará de um banco de dados ou arquivo seguro
    # Por enquanto, criamos um espaço na memória
    if "configs" not in st.session_state:
        st.session_state["configs"] = {}
    return st.session_state["configs"].get(nome_projeto, {})

# --- PÁGINAS ---

if page == "🏠 Dados Consolidados":
    st.title(f"📊 Consolidado: {projeto_ativo}")
    st.write(f"Exibindo métricas exclusivas do **{projeto_ativo}**.")

elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Lead Scoring - {projeto_ativo}")
    # O link do Sheets agora é salvo por projeto
    link_key = f"sheets_{projeto_ativo}"
    url = st.text_input("Link CSV do Sheets deste projeto", key=link_key)
    if url:
        st.success(f"Planilha vinculada ao {projeto_ativo}")

elif page == "🔌 Conexões":
    st.title(f"🔌 Configurações: {projeto_ativo}")
    st.subheader(f"Configure as APIs para o {projeto_ativo}")
    
    # Campos que mudam conforme o projeto selecionado
    col1, col2 = st.columns(2)
    with col1:
        st.text_input(f"Token Meta Ads ({projeto_ativo})", type="password")
        st.text_input(f"ID da Conta de Anúncios", placeholder="act_123456")
    with col2:
        st.text_input(f"API Key Kiwify ({projeto_ativo})", type="password")
        st.text_input(f"Secret Hotmart", type="password")

# --- MANTENDO AS OUTRAS PÁGINAS (SEM ALTERAÇÕES) ---
elif page == "🔵 Meta Ads":
    st.title(f"🔵 Meta Ads - {projeto_ativo}")
elif page == "🔴 Google Ads":
    st.title(f"🔴 Google Ads - {projeto_ativo}")
elif page == "⚫ TikTok Ads":
    st.title(f"⚫ TikTok Ads - {projeto_ativo}")
elif page == "🟠 Hotmart":
    st.title(f"🟠 Hotmart - {projeto_ativo}")
elif page == "🟢 Kiwify":
    st.title(f"🟢 Kiwify - {projeto_ativo}")
elif page == "🌪️ Funil de Perpétuo":
    st.title(f"🌪️ Funil de Perpétuo - {projeto_ativo}")
