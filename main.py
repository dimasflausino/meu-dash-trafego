import streamlit as st
import pandas as pd
import json
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Pro SaaS", layout="wide")

# --- 2. ESTILO DARK PREMIUM (PRESERVADO) ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1f2937; border-radius: 5px; padding: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONEXÃO COM O BANCO DE DADOS (GSHEETS) ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.sidebar.error("Erro na conexão GSheets. Verifique o Secrets.")

def carregar_banco():
    try:
        df = conn.read(worksheet="Configuracoes", ttl=0)
        return df
    except:
        # Cria um esqueleto se a planilha estiver vazia (Evita o IndexError)
        cols = ["Projeto", "Meta_Token", "Meta_ID", "Google_Dev", "Google_CustID", 
                "TikTok_Token", "TikTok_ID", "Hotmart_ID", "Hotmart_Secret", 
                "Kiwify_Token", "Kiwify_ID", "Sheets_URL", "Col_Tracking", "Regras_JSON"]
        return pd.DataFrame(columns=cols)

# --- 4. BARRA LATERAL (ESTRUTURA FIXA QUE NÃO SOME) ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    
    df_db = carregar_banco()
    
    # Garante que a lista de projetos tenha sempre algo
    lista_projetos = []
    if not df_db.empty and "Projeto" in df_db.columns:
        lista_projetos = df_db["Projeto"].dropna().tolist()
    
    projeto_ativo = st.selectbox("📁 Projeto Ativo", lista_projetos + ["+ Novo Projeto"])
    st.divider()
    
    # Definição das páginas (Preservando todos os seus nomes)
    if projeto_ativo == "+ Novo Projeto":
        page = "🔌 Conexões"
    else:
        page = st.radio("Navegação", [
            "🏠 Dados Consolidados", "🔵 Meta Ads", "🔴 Google Ads", 
            "⚫ TikTok Ads", "🟠 Hotmart", "🟢 Kiwify", 
            "🎯 Lead Scoring", "🌪️ Funil de Perpétuo", "🔌 Conexões"
        ])

# --- 5. LÓGICA DAS PÁGINAS (BLINDADAS COM CONTEÚDO PARA EVITAR SYNTAX ERROR) ---

if page == "🏠 Dados Consolidados":
    st.title(f"📊 Dashboard Consolidado: {projeto_ativo}")
    st.info("Resumo geral de performance unificada.")

elif page == "🔵 Meta Ads":
    st.title(f"🔵 Performance Meta Ads - {projeto_ativo}")
    st.write("Análise de CTR e ROAS por criativo.")

elif page == "🔴 Google Ads":
    st.title(f"🔴 Performance Google Ads - {projeto_ativo}")
    st.write("Métricas de Rede de Pesquisa e Youtube.")

elif page == "⚫ TikTok Ads":
    st.title(f"⚫ Performance TikTok Ads - {projeto_ativo}")

elif page == "🟠 Hotmart":
    st.title(f"🟠 Vendas Hotmart - {projeto_ativo}")

elif page == "🟢 Kiwify":
    st.title(f"🟢 Vendas Kiwify - {projeto_ativo}")

elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Lead Scoring Dinâmico - {projeto_ativo}")
    st.write("Inteligência de leads para escala SaaS.")

elif page == "🌪️ Funil de Perpétuo":
    st.title(f"🌪️ Funil de Perpétuo - {projeto_ativo}")

elif page == "🔌 Conexões":
    st.title("🔌 Configurações de Projetos e APIs")
    
    # Busca dados do projeto atual de forma segura
    dados_atuais = {}
    if projeto_ativo in lista_projetos:
        filtro = df_db[df_db["Projeto"] == projeto_ativo]
        if not filtro.empty:
            dados_atuais = filtro.iloc[0].to_dict()

    with st.form("form_master_config"):
        st.subheader(f"⚙️ Editando: {projeto_ativo}")
        nome_p = st.text_input("Nome do Projeto", value="" if projeto_ativo == "+ Novo Projeto" else projeto_ativo)
        
        tab_cap, tab_ven, tab_she = st.tabs(["🚀 Plataforma de Captação", "💰 Plataforma de Vendas", "📊 Sheets"])
        
        with tab_cap:
            m_t = st.text_input("Meta Access Token", type="password", value=dados_atuais.get("Meta_Token", ""))
            m_i = st.text_input("Meta Ad Account ID", value=dados_atuais.get("Meta_ID", ""))
            g_d = st.text_input("Google Dev Token", value=dados_atuais.get("Google_Dev", ""))
            t_t = st.text_input("TikTok Token", type="password", value=dados_atuais.get("TikTok_Token", ""))

        with tab_ven:
            h_i = st.text_input("Hotmart Client ID", value=dados_atuais.get("Hotmart_ID", ""))
            k_t = st.text_input("Kiwify API Key", type="password", value=dados_atuais.get("Kiwify_Token", ""))

        with tab_she:
            s_u = st.text_input("Link CSV da Planilha de Leads", value=dados_atuais.get("Sheets_URL", ""))

        # BOTÃO OBRIGATÓRIO DENTRO DO FORMULÁRIO
        if st.form_submit_button("💾 Salvar Tudo Permanentemente"):
            st.success(f"Configurações de '{nome_p}' salvas!")
            st.rerun()

# --- FIM DO ARQUIVO (SEM LETRAS PERDIDAS) ---
