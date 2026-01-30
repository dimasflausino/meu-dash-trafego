import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Pro 2026", layout="wide")

# --- CSS DARK PREMIUM (PRESERVADO) ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM A PLANILHA MESTRA (DATABASE) ---
# Lembre-se de configurar o arquivo .streamlit/secrets.toml com o link da planilha
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Erro na conexão com o Google Sheets. Verifique as chaves em Conexões.")

def carregar_projetos():
    try:
        # Tenta ler a aba 'Configuracoes' da sua planilha mestra
        return conn.read(worksheet="Configuracoes", ttl=0)
    except:
        # Se falhar (ex: planilha vazia), cria uma estrutura padrão
        return pd.DataFrame(columns=["Projeto", "Meta_Token", "Google_Token", "TikTok_Token", "Hotmart_Token", "Kiwify_Token", "Sheets_URL"])

# --- MENU LATERAL (TODOS OS ITENS RESTAURADOS) ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    
    # Carrega a lista de projetos do banco de dados (Sheets)
    df_db = carregar_projetos()
    lista_projetos = df_db["Projeto"].tolist() if not df_db.empty else ["Projeto Padrão"]
    
    projeto_ativo = st.selectbox("📁 Projeto Ativo", lista_projetos + ["+ Novo Projeto"])
    st.divider()
    
    # Menu completo sem omissões
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

# --- LÓGICA DAS PÁGINAS ---

if page == "🏠 Dados Consolidados":
    st.title(f"📊 Dashboard Consolidado: {projeto_ativo}")
    st.write("Visão geral de ROI e Faturamento unificado.")

elif page == "🔵 Meta Ads":
    st.title(f"🔵 Performance Meta Ads - {projeto_ativo}")
    st.write("Dados extraídos da Marketing API v24.0.")

elif page == "🔴 Google Ads":
    st.title(f"🔴 Performance Google Ads - {projeto_ativo}")
    st.write("Análise de campanhas de Busca e Youtube.")

elif page == "⚫ TikTok Ads":
    st.title(f"⚫ Performance TikTok Ads - {projeto_ativo}")
    st.write("Métricas de conversão de anúncios em vídeo.")

elif page == "🟠 Hotmart":
    st.title(f"🟠 Vendas Hotmart - {projeto_ativo}")

elif page == "🟢 Kiwify":
    st.title(f"🟢 Vendas Kiwify - {projeto_ativo}")

elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Lead Scoring & Qualidade - {projeto_ativo}")
    st.subheader("Cruzamento: Meta Ads vs. Leads do Sheets")
    # Aqui a lógica usará a Sheets_URL salva para este projeto

elif page == "🌪️ Funil de Perpétuo":
    st.title(f"🌪️ Funil de Perpétuo - {projeto_ativo}")

elif page == "🔌 Conexões":
    st.title("🔌 Configurações de Projetos")
    
    with st.form("form_config"):
        st.subheader(f"⚙️ Cadastro/Edição: {projeto_ativo}")
        nome = st.text_input("Nome do Projeto", value="" if projeto_ativo == "+ Novo Projeto" else projeto_ativo)
        
        c1, c2 = st.columns(2)
        with c1:
            m_token = st.text_input("Token Meta Ads", type="password")
            g
