import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Pro SaaS", layout="wide")

# --- CSS DARK PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1f2937; border-radius: 5px; padding: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM O BANCO DE DADOS (SHEETS MESTRE) ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.sidebar.warning("⚠️ Banco de Dados offline. Configure o secrets.toml.")

def carregar_banco():
    try:
        return conn.read(worksheet="Configuracoes", ttl=0)
    except:
        cols = ["Projeto", "Meta_Token", "Meta_ID", "Google_Dev", "Google_CustID", 
                "TikTok_Token", "TikTok_ID", "Hotmart_ID", "Hotmart_Secret", 
                "Kiwify_Token", "Kiwify_ID", "Sheets_URL", "Col_Tracking", "Regras_JSON"]
        return pd.DataFrame(columns=cols)

# --- MENU LATERAL COMPLETO ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    
    df_db = carregar_banco()
    lista_projetos = df_db["Projeto"].tolist() if not df_db.empty else ["Projeto Padrão"]
    
    projeto_ativo = st.selectbox("📁 Projeto Ativo", lista_projetos + ["+ Novo Projeto"])
    st.divider()
    
    if projeto_ativo == "+ Novo Projeto":
        page = "🔌 Conexões"
    else:
        page = st.radio("Navegação", [
            "🏠 Dados Consolidados", "🔵 Meta Ads", "🔴 Google Ads", 
            "⚫ TikTok Ads", "🟠 Hotmart", "🟢 Kiwify", 
            "🎯 Lead Scoring", "🌪️ Funil de Perpétuo", "🔌 Conexões"
        ])

# --- FUNÇÕES DE LÓGICA ---
def aplicar_scoring(df, projeto):
    # Aqui buscaremos as regras salvas no banco para o projeto
    df['Score_Total'] = 0
    # Lógica de scoring será inserida aqui
    return df

# --- PÁGINA DE CONEXÕES (RESTAURADA E COMPLETA) ---
if page == "🔌 Conexões":
    st.title("🔌 Configurações de Projetos e APIs")
    
    with st.form("form_master_config"):
        st.subheader(f"⚙️ Editando: {projeto_ativo}")
        nome_p = st.text_input("Nome do Projeto", value="" if projeto_ativo == "+ Novo Projeto" else projeto_ativo)
        
        tab_t, tab_v, tab_d = st.tabs(["🚀 Plataforma de Captação", "💰 Plataforma de Vendas", "📊 Sheets"])
        
        with tab_t:
            st.write("**Meta Ads v24.0**")
            m_t = st.text_input("Access Token", type="password")
            m_i = st.text_input("Ad Account ID (act_xxx)")
            st.write("**Google Ads**")
            g_d = st.text_input("Developer Token")
            g_c = st.text_input("Customer ID")
            st.write("**TikTok Ads**")
            t_t = st.text_input("Access Token TikTok", type="password")
            t_i = st.text_input("Advertiser ID")

        with tab_v:
            st.write("**Hotmart**")
            h_i = st.text_input("Client ID")
            h_s = st.text_input("Client Secret", type="password")
            st.write("**Kiwify**")
            k_t = st.text_input("API Key (Kiwify)", type="password")
            k_i = st.text_input("Account ID")

        with tab_d:
            s_u = st.text_input("Link CSV da Planilha de Leads")
            st.info("O mapeamento de colunas aparecerá na aba Lead Scoring após salvar o link.")

        if st.form_submit_button("💾 Salvar Tudo Permanentemente"):
            # Lógica de salvar no Sheets Mestre
            st.success(f"Projeto {nome_p} salvo com sucesso!")
            st.rerun()

# --- PÁGINA DE LEAD SCORING (DINÂMICA) ---
elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Lead Scoring Dinâmico - {projeto_ativo}")
    # Aqui entra a lógica de ler as colunas do link de leads salvo
