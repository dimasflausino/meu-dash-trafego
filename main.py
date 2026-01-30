import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Pro 2026", layout="wide")

# --- CSS DARK PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM O BANCO DE DADOS (SHEETS) ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Erro de conexão. Certifique-se de configurar o secrets.toml no Streamlit Cloud.")

def carregar_projetos():
    try:
        return conn.read(worksheet="Configuracoes", ttl=0)
    except:
        # Estrutura completa baseada nas APIs de 2026
        cols = ["Projeto", "Meta_Token", "Meta_ID", "Google_Dev", "Google_CustID", 
                "TikTok_Token", "TikTok_ID", "Hotmart_ID", "Hotmart_Secret", 
                "Kiwify_Token", "Kiwify_ID", "Sheets_URL"]
        return pd.DataFrame(columns=cols)

# --- MENU LATERAL ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    
    df_db = carregar_projetos()
    lista_projetos = df_db["Projeto"].tolist() if not df_db.empty else []
    
    projeto_ativo = st.selectbox("📁 Projeto Ativo", lista_projetos + ["+ Novo Projeto"])
    st.divider()
    
    page = st.radio("Navegação", [
        "🏠 Dados Consolidados", "🔵 Meta Ads", "🔴 Google Ads", 
        "⚫ TikTok Ads", "🟠 Hotmart", "🟢 Kiwify", 
        "🎯 Lead Scoring", "🌪️ Funil de Perpétuo", "🔌 Conexões"
    ])

# --- LÓGICA DAS PÁGINAS ---

if page == "🔌 Conexões":
    st.title("🔌 Configurações de Projetos")
    
    # O formulário agora tem o botão de submit obrigatório no final
    with st.form("form_config_geral"):
        st.subheader(f"⚙️ Configurando: {projeto_ativo}")
        nome = st.text_input("Nome do Projeto", value="" if projeto_ativo == "+ Novo Projeto" else projeto_ativo)
        
        tab1, tab2, tab3 = st.tabs(["Tráfego (Meta/Google/TT)", "Vendas (Hot/Kiwi)", "Dados (Sheets)"])
        
        with tab1:
            st.write("**Meta Ads**")
            m_t = st.text_input("Access Token", type="password")
            m_i = st.text_input("Ad Account ID (act_xxx)")
            st.write("**Google Ads**")
            g_d = st.text_input("Developer Token")
            g_c = st.text_input("Customer ID")
            st.write("**TikTok Ads**")
            t_t = st.text_input("Access Token TikTok", type="password")
            t_i = st.text_input("Advertiser ID")

        with tab2:
            st.write("**Hotmart**")
            h_i = st.text_input("Client ID")
            h_s = st.text_input("Client Secret", type="password")
            st.write("**Kiwify**")
            k_t = st.text_input("API Key (Kiwify)", type="password")
            k_i = st.text_input("Account ID")

        with tab3:
            s_u = st.text_input("Link CSV da Planilha de Leads")

        # O BOTÃO QUE ESTAVA FALTANDO
        enviar = st.form_submit_button("💾 Salvar Configurações Permanentemente")

        if enviar:
            novo_projeto = pd.DataFrame([{
                "Projeto": nome, "Meta_Token": m_t, "Meta_ID": m_i,
                "Google_Dev": g_d, "Google_CustID": g_c,
                "TikTok_Token": t_t, "TikTok_ID": t_i,
                "Hotmart_ID": h_i, "Hotmart_Secret": h_s,
                "Kiwify_Token": k_t, "Kiwify_ID": k_i,
                "Sheets_URL": s_u
            }])
            
            df_final = pd.concat([df_db, novo_projeto]).drop_duplicates(subset=['Projeto'], keep='last')
            conn.update(worksheet="Configuracoes", data=df_final)
            st.success(f"Projeto '{nome}' atualizado no banco de dados!")
            st.rerun()

elif page == "🏠 Dados Consolidados":
    st.title(f"📊 Dashboard: {projeto_ativo}")
    st.info("Aguardando configuração de APIs para exibir dados reais.")

# As outras páginas mantêm o título do projeto ativo
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
elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Lead Scoring - {projeto_ativo}")
elif page == "🌪️ Funil de Perpétuo":
    st.title(f"🌪️ Funil de Perpétuo - {projeto_ativo}")
