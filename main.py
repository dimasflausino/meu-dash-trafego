import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Pro - Multi-Projeto 2026", layout="wide")

# --- INICIALIZAÇÃO DA MEMÓRIA (BANCO DE DADOS TEMPORÁRIO) ---
if "banco_projetos" not in st.session_state:
    st.session_state["banco_projetos"] = {
        "Projeto Exemplo": {
            "meta_token": "", "meta_account_id": "",
            "google_dev_token": "", "google_customer_id": "",
            "kiwify_id": "", "kiwify_secret": "",
            "sheets_leads": ""
        }
    }

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

# --- MENU LATERAL ---
with st.sidebar:
    st.title("🛡️ Painel Administrativo")
    
    lista_projetos = list(st.session_state["banco_projetos"].keys())
    projeto_ativo = st.selectbox("📁 Selecione o Projeto", lista_projetos + ["+ Criar Novo Projeto"])
    
    st.divider()
    
    # Se o usuário selecionar a opção de criar, ele trava na aba de conexões
    if projeto_ativo == "+ Criar Novo Projeto":
        page = "🔌 Conexões"
    else:
        page = st.radio("Navegação", [
            "🏠 Dados Consolidados", "🔵 Meta Ads", "🔴 Google Ads", 
            "⚫ TikTok Ads", "🟠 Hotmart", "🟢 Kiwify", 
            "🎯 Lead Scoring", "🌪️ Funil de Perpétuo", "🔌 Conexões"
        ])

# --- LÓGICA DAS PÁGINAS ---

if page == "🔌 Conexões":
    st.title("🔌 Configurações de API por Projeto")
    
    if projeto_ativo == "+ Criar Novo Projeto":
        st.subheader("🆕 Cadastro de Novo Projeto")
        with st.form("form_novo_projeto"):
            nome_projeto = st.text_input("Nome do Projeto/Cliente")
            st.info("Ao clicar em salvar, o projeto será adicionado à lista lateral.")
            if st.form_submit_button("Salvar e Iniciar Configuração"):
                if nome_projeto and nome_projeto not in st.session_state["banco_projetos"]:
                    st.session_state["banco_projetos"][nome_projeto] = {}
                    st.success(f"Projeto '{nome_projeto}' criado! Agora configure os tokens abaixo.")
                    st.rerun()

    else:
        st.subheader(f"⚙️ Editando: {projeto_ativo}")
        
        # ABAS PARA CADA PLATAFORMA (DOCUMENTAÇÃO 2026)
        tab_meta, tab_google, tab_vendas, tab_leads = st.tabs(["Meta Ads", "Google Ads", "Checkouts", "Sheets & Leads"])
        
        with tab_meta:
            st.write("### Integração Meta Ads v24.0")
            st.text_input("Access Token (System User)", type="password", key=f"mt_{projeto_ativo}")
            st.text_input("Ad Account ID (act_xxxxxxxx)", placeholder="act_", key=f"mid_{projeto_ativo}")
            
        with tab_google:
            st.write("### Google Ads API")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Developer Token", key=f"gdev_{projeto_ativo}")
                st.text_input("Customer ID", key=f"gcid_{projeto_ativo}")
            with col2:
                st.text_input("Client ID", key=f"gcli_{projeto_ativo}")
                st.text_input("Refresh Token", type="password", key=f"gref_{projeto_ativo}")

        with tab_vendas:
            st.write("### Hotmart & Kiwify")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Hotmart**")
                st.text_input("Client ID", key=f"hcli_{projeto_ativo}")
                st.text_input("Client Secret", type="password", key=f"hsec_{projeto_ativo}")
            with col2:
                st.write("**Kiwify**")
                st.text_input("Client ID (API Key)", key=f"kcli_{projeto_ativo}")
                st.text_input("Client Secret", type="password", key=f"ksec_{projeto_ativo}")

        with tab_leads:
            st.write("### Google Sheets (Lead Scoring)")
            st.text_input("URL do CSV da Planilha de Leads", key=f"sheet_{projeto_ativo}")
            st.text_input("Coluna do Nome do Ad (UTM)", value="utm_content", key=f"utm_{projeto_ativo}")

        if st.button("💾 Salvar Configurações do Projeto"):
            st.success(f"Configurações de '{projeto_ativo}' salvas com sucesso!")

# --- PÁGINA DE VISÃO GERAL ---
elif page == "🏠 Dados Consolidados":
    st.title(f"📊 Consolidado: {projeto_ativo}")
    st.metric("ROI Global", "4.5x", delta="0.2x")
    st.write(f"Conectado ao Sheets: {st.session_state.get(f'sheet_{projeto_ativo}', 'Não configurado')}")

# (As outras páginas seguem a mesma lógica de projeto_ativo...)
