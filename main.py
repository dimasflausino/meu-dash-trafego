import streamlit as st
import pandas as pd
import json
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURAÇÃO DA PÁGINA (Deve ser a primeira linha) ---
st.set_page_config(page_title="Analytics Pro SaaS", layout="wide")

# --- 2. ESTILO DARK PREMIUM ---
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
def carregar_banco():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Configuracoes", ttl=0)
        return df, conn
    except:
        # Estrutura de backup caso a planilha esteja vazia ou offline
        cols = ["Projeto", "Meta_Token", "Meta_ID", "Google_Dev", "Google_CustID", 
                "TikTok_Token", "TikTok_ID", "Hotmart_ID", "Hotmart_Secret", 
                "Kiwify_Token", "Kiwify_ID", "Sheets_URL", "Col_Tracking", "Regras_JSON"]
        return pd.DataFrame(columns=cols), None

df_db, conn = carregar_banco()

# --- 4. BARRA LATERAL (ESTRUTURA FIXA) ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    
    # Lista de projetos segura
    lista_p = []
    if not df_db.empty and "Projeto" in df_db.columns:
        lista_p = df_db["Projeto"].dropna().unique().tolist()
    
    projeto_ativo = st.selectbox("📁 Projeto Ativo", lista_p + ["+ Novo Projeto"])
    st.divider()
    
    # Navegação completa (Nomes preservados)
    if projeto_ativo == "+ Novo Projeto":
        page = "🔌 Conexões"
    else:
        page = st.radio("Navegação", [
            "🏠 Dados Consolidados", "🔵 Meta Ads", "🔴 Google Ads", 
            "⚫ TikTok Ads", "🟠 Hotmart", "🟢 Kiwify", 
            "🎯 Lead Scoring", "🌪️ Funil de Perpétuo", "🔌 Conexões"
        ])
    st.divider()
    st.info(f"Logado: {projeto_ativo}")

# --- 5. LÓGICA DAS PÁGINAS (BLINDADAS CONTRA BLOCOS VAZIOS) ---

if page == "🏠 Dados Consolidados":
    st.title(f"📊 Dashboard Consolidado: {projeto_ativo}")
    st.write("Visão geral de ROI, Investimento e Faturamento.")

elif page == "🔵 Meta Ads":
    st.title(f"🔵 Meta Ads - {projeto_ativo}")
    st.info("Métricas de performance do Facebook e Instagram.")

elif page == "🔴 Google Ads":
    st.title(f"🔴 Google Ads - {projeto_ativo}")
    st.info("Performance de busca e Youtube Ads.")

elif page == "⚫ TikTok Ads":
    st.title(f"⚫ TikTok Ads - {projeto_ativo}")
    st.info("Análise de conversão de vídeos.")

elif page == "🟠 Hotmart":
    st.title(f"🟠 Hotmart - {projeto_ativo}")
    st.write("Acompanhamento de vendas e checkouts.")

elif page == "🟢 Kiwify":
    st.title(f"🟢 Kiwify - {projeto_ativo}")
    st.write("Faturamento e volume de transações.")

elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Lead Scoring Dinâmico - {projeto_ativo}")
    st.write("Defina as regras de pontuação para qualificar seus leads.")

elif page == "🌪️ Funil de Perpétuo":
    st.title(f"🌪️ Funil de Perpétuo - {projeto_ativo}")
    st.write("Taxas de conversão de Order Bump e Upsells.")

elif page == "🔌 Conexões":
    st.title("🔌 Configurações de Projetos")
    
    # Busca de dados segura (Resolve o IndexError)
    dados = {}
    if projeto_ativo in lista_p:
        temp = df_db[df_db["Projeto"] == projeto_ativo]
        if not temp.empty:
            dados = temp.iloc[0].to_dict()

    with st.form("form_config_geral"):
        st.subheader(f"⚙️ Configurando: {projeto_ativo}")
        novo_nome = st.text_input("Nome do Projeto", value="" if projeto_ativo == "+ Novo Projeto" else projeto_ativo)
        
        tab1, tab2, tab3 = st.tabs(["🚀 Plataforma de Captação", "💰 Plataforma de Vendas", "📊 Sheets"])
        
        with tab1:
            m_t = st.text_input("Meta Token", type="password", value=dados.get("Meta_Token", ""))
            m_i = st.text_input("Meta ID", value=dados.get("Meta_ID", ""))
            g_d = st.text_input("Google Dev Token", value=dados.get("Google_Dev", ""))
            t_t = st.text_input("TikTok Token", type="password", value=dados.get("TikTok_Token", ""))

        with tab2:
            h_i = st.text_input("Hotmart ID", value=dados.get("Hotmart_ID", ""))
            k_t = st.text_input("Kiwify API Key", type="password", value=dados.get("Kiwify_Token", ""))
            
        with tab3:
            s_u = st.text_input("Link CSV do Sheets", value=dados.get("Sheets_URL", ""))

        # BOTÃO OBRIGATÓRIO (Resolve o Missing Submit Button)
        if st.form_submit_button("💾 Salvar Configurações"):
            st.success(f"Configuração de '{novo_nome}' enviada!")
            st.rerun()

# --- FIM DO ARQUIVO (LIMPO E SEM LETRAS PERDIDAS) ---
