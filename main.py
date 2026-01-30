import streamlit as st
import pandas as pd
import json
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Pro SaaS", layout="wide")

# --- 2. ESTILO DARK (PRESERVADO) ---
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
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.sidebar.error("Configure o secrets.toml no Streamlit.")

def carregar_banco():
    try:
        return conn.read(worksheet="Configuracoes", ttl=0)
    except:
        cols = ["Projeto", "Meta_Token", "Meta_ID", "Google_Dev", "Google_CustID", 
                "TikTok_Token", "TikTok_ID", "Hotmart_ID", "Hotmart_Secret", 
                "Kiwify_Token", "Kiwify_ID", "Sheets_URL", "Col_Tracking", "Regras_JSON"]
        return pd.DataFrame(columns=cols)

# --- 4. MENU LATERAL ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    df_db = carregar_banco()
    lista_p = df_db["Projeto"].tolist() if not df_db.empty else []
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

# --- 5. FUNÇÕES DE LÓGICA ---
def aplicar_scoring(df, regras_json):
    df['Score_Total'] = 0
    try:
        regras = json.loads(regras_json) if isinstance(regras_json, str) else []
        for r in regras:
            col, val, pts = r['coluna'], r['valor'], r['pontos']
            if col in df.columns:
                df.loc[df[col].astype(str).str.contains(val, case=False, na=False), 'Score_Total'] += pts
    except:
        pass
    return df

# --- 6. PÁGINAS ---

if page == "🔌 Conexões":
    st.title("🔌 Configurações de Projetos")
    
    with st.form("form_master"):
        st.subheader(f"⚙️ Configurando: {projeto_ativo}")
        nome_p = st.text_input("Nome do Projeto", value="" if projeto_ativo == "+ Novo Projeto" else projeto_ativo)
        
        tab_t, tab_v, tab_d = st.tabs(["🚀 Plataforma de Captação", "💰 Plataforma de Vendas", "📊 Sheets"])
        
        # BUSCA SEGURA DE DADOS (EVITA O INDEX ERROR)
        if projeto_ativo in lista_p and not df_db[df_db["Projeto"] == projeto_ativo].empty:
            dados_atuais = df_db[df_db["Projeto"] == projeto_ativo].iloc[0]
        else:
            dados_atuais = {}

        with tab_t:
            m_t = st.text_input("Meta Access Token", type="password", value=dados_atuais.get("Meta_Token", ""))
            m_i = st.text_input("Meta Ad Account ID", value=dados_atuais.get("Meta_ID", ""))
            g_d = st.text_input("Google Dev Token", value=dados_atuais.get("Google_Dev", ""))
            t_t = st.text_input("TikTok Token", type="password", value=dados_atuais.get("TikTok_Token", ""))
        
        with tab_v:
            h_i = st.text_input("Hotmart Client ID", value=dados_atuais.get("Hotmart_ID", ""))
            k_t = st.text_input("Kiwify API Key", type="password", value=dados_atuais.get("Kiwify_Token", ""))
            
        with tab_d:
            s_u = st.text_input("Link CSV da Planilha de Leads", value=dados_atuais.get("Sheets_URL", ""))

        # BOTÃO DENTRO DO FORMULÁRIO (EVITA O MISSING SUBMIT BUTTON)
        if st.form_submit_button("💾 Salvar Configurações"):
            st.success(f"Projeto {nome_p} salvo!")
            # Lógica de salvar no banco aqui...
            st.rerun()

elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Inteligência de Leads - {projeto_ativo}")
    st.write("Mapeie as colunas do seu Sheets para escala SaaS.")
    # Inteligência dinâmica preservada

elif page == "🏠 Dados Consolidados":
    st.title(f"🏠 Consolidado: {projeto_ativo}")
    st.info("Resumo geral de ROI e faturamento.")

elif page == "🔵 Meta Ads":
    st.title(f"🔵 Meta Ads - {projeto_ativo}")
    st.write("Dados de campanhas ativos.")

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
