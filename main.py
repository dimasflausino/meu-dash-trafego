import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Pro - Multi-Projeto", layout="wide")

# --- INICIALIZAÇÃO DA MEMÓRIA (LISTA DE PROJETOS) ---
if "meus_projetos" not in st.session_state:
    # Começamos com um projeto padrão
    st.session_state["meus_projetos"] = ["Projeto Padrão"]

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
    
    # O Seletor agora lê a lista que está na memória
    projeto_ativo = st.selectbox("📁 Projeto Ativo", st.session_state["meus_projetos"])
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

# --- PÁGINAS ---

if page == "🏠 Dados Consolidados":
    st.title(f"📊 Consolidado: {projeto_ativo}")
    st.write("Visão geral de ROI e Faturamento deste projeto.")

elif page == "🔌 Conexões":
    st.title("🔌 Gerenciar Projetos e APIs")
    
    # --- SEÇÃO PARA CRIAR NOVO PROJETO ---
    st.subheader("🆕 Cadastrar Novo Projeto")
    with st.container(border=True):
        novo_nome = st.text_input("Nome do Novo Projeto (Ex: Lançamento X)")
        if st.button("➕ Criar Projeto"):
            if novo_nome and novo_nome not in st.session_state["meus_projetos"]:
                st.session_state["meus_projetos"].append(novo_nome)
                st.success(f"Projeto '{novo_nome}' criado com sucesso!")
                st.rerun() # Atualiza a tela para o projeto aparecer no menu lateral
            else:
                st.error("Nome inválido ou projeto já existente.")

    st.divider()
    
    # --- SEÇÃO PARA CONFIGURAR APIs DO PROJETO ATIVO ---
    st.subheader(f"⚙️ Configurações de API: {projeto_ativo}")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input(f"Token Meta Ads - {projeto_ativo}", type="password")
    with c2:
        st.text_input(f"Token Kiwify - {projeto_ativo}", type="password")

# --- MANTENDO AS OUTRAS PÁGINAS ---
elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Lead Scoring - {projeto_ativo}")
    st.text_input(f"Link CSV do Sheets ({projeto_ativo})")

elif page == "🔵 Meta Ads":
    st.title(f"🔵 Meta Ads - {projeto_ativo}")

# (As outras páginas continuam seguindo a mesma lógica...)
