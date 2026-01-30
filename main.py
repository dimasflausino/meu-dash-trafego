import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Pro 2026", layout="wide")

# --- CONEXÃO COM A PLANILHA MESTRA (BANCO DE DADOS) ---
# Aqui o app se conecta à sua planilha de configurações
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_projetos():
    try:
        return conn.read(worksheet="Configuracoes", ttl=0)
    except:
        return pd.DataFrame(columns=["Projeto", "Meta_Token", "Kiwify_Token", "Sheets_URL"])

# --- MENU LATERAL ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    df_projetos = carregar_projetos()
    lista_nomes = df_projetos["Projeto"].tolist() if not df_projetos.empty else []
    
    projeto_ativo = st.selectbox("📁 Projeto Ativo", lista_nomes + ["+ Novo Projeto"])
    st.divider()
    
    page = st.radio("Navegação", [
        "🏠 Dados Consolidados", "🔵 Meta Ads", "🟢 Kiwify", 
        "🎯 Lead Scoring", "🔌 Conexões"
    ])

# --- PÁGINA DE CONEXÕES (ONDE A MÁGICA ACONTECE) ---
if page == "🔌 Conexões":
    st.title("🔌 Configurações de Projetos")
    
    with st.form("form_projeto"):
        nome = st.text_input("Nome do Projeto", value="" if projeto_ativo == "+ Novo Projeto" else projeto_ativo)
        token_meta = st.text_input("Token Meta Ads", type="password")
        token_kiwi = st.text_input("Token Kiwify", type="password")
        url_leads = st.text_input("Link CSV Leads (Google Sheets)")
        
        if st.form_submit_button("💾 Salvar Projeto Permanentemente"):
            # Lógica para salvar na Planilha Mestra
            novo_dado = pd.DataFrame([{
                "Projeto": nome,
                "Meta_Token": token_meta,
                "Kiwify_Token": token_kiwi,
                "Sheets_URL": url_leads
            }])
            # Atualiza a planilha (Isso aqui substitui o banco de dados caro)
            df_atualizado = pd.concat([df_projetos, novo_dado]).drop_duplicates(subset=['Projeto'], keep='last')
            conn.update(worksheet="Configuracoes", data=df_atualizado)
            st.success(f"Projeto {nome} salvo com sucesso!")
            st.rerun()

# --- PÁGINA DE LEAD SCORING ---
elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Lead Scoring: {projeto_ativo}")
    if projeto_ativo != "+ Novo Projeto":
        dados_projeto = df_projetos[df_projetos["Projeto"] == projeto_ativo].iloc[0]
        st.write(f"Conectado à planilha: {dados_projeto['Sheets_URL']}")
        # Aqui o código puxa os leads usando a URL salva
    else:
        st.warning("Selecione um projeto válido para ver o Lead Scoring.")
