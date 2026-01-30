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
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO BANCO DE DADOS (MEMÓRIA) ---
if "banco_projetos" not in st.session_state:
    st.session_state["banco_projetos"] = {
        "Projeto Padrão": {
            "coluna_tracking": "utm_content",
            "regras_score": [],
            "url_sheets": ""
        }
    }

# --- MENU LATERAL ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    lista_projetos = list(st.session_state["banco_projetos"].keys())
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

# --- FUNÇÃO DE CÁLCULO DE SCORE ---
def aplicar_scoring(df, regras):
    df['Score_Total'] = 0
    for r in regras:
        col, val, pts = r['coluna'], r['valor'], r['pontos']
        if col in df.columns:
            df.loc[df[col].astype(str).str.contains(val, case=False, na=False), 'Score_Total'] += pts
    return df

# --- LÓGICA DAS PÁGINAS ---

if page == "🔌 Conexões":
    st.title("🔌 Configurações e Mapeamento")
    
    if projeto_ativo == "+ Novo Projeto":
        with st.form("novo_p"):
            nome = st.text_input("Nome do Novo Projeto")
            if st.form_submit_button("Criar"):
                st.session_state["banco_projetos"][nome] = {"regras_score": [], "url_sheets": ""}
                st.rerun()
    else:
        st.subheader(f"⚙️ Ajustando: {projeto_ativo}")
        url = st.text_input("Link CSV do Sheets (Leads)", value=st.session_state["banco_projetos"][projeto_ativo].get("url_sheets", ""))
        
        if url:
            try:
                # Preview de Colunas para facilitar o SaaS
                df_preview = pd.read_csv(url.replace('/edit#gid=', '/export?format=csv&gid='))
                colunas_detectadas = df_preview.columns.tolist()
                
                st.success("✅ Planilha conectada! Mapeie os dados abaixo:")
                
                c1, c2 = st.columns(2)
                with c1:
                    col_track = st.selectbox("Coluna de Tracking (UTM)", colunas_detectadas)
                with c2:
                    st.write("**Regras de Pontuação Ativas:**")
                    st.write(st.session_state["banco_projetos"][projeto_ativo]["regras_score"])

                # Adicionar Novas Regras
                with st.expander("➕ Adicionar Regra de Pontuação"):
                    col_alvo = st.selectbox("Se a coluna...", colunas_detectadas)
                    val_alvo = st.text_input("Contiver o texto...")
                    pts_alvo = st.number_input("Ganhe X pontos", value=10)
                    if st.button("Salvar Regra"):
                        st.session_state["banco_projetos"][projeto_ativo]["regras_score"].append(
                            {"coluna": col_alvo, "valor": val_alvo, "pontos": pts_alvo}
                        )
                        st.rerun()
                
                if st.button("💾 Salvar Configuração do Projeto"):
                    st.session_state["banco_projetos"][projeto_ativo]["url_sheets"] = url
                    st.session_state["banco_projetos"][projeto_ativo]["coluna_tracking"] = col_track
                    st.success("Tudo salvo!")
            except:
                st.error("Erro ao ler o link. Verifique se ele termina em /edit#gid=... e está aberto ao público.")

elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Lead Scoring: {projeto_ativo}")
    config = st.session_state["banco_projetos"].get(projeto_ativo, {})
    url = config.get("url_sheets", "")
    
    if url:
        df = pd.read_csv(url.replace('/edit#gid=', '/export?format=csv&gid='))
        df = aplicar_scoring(df, config.get("regras_score", []))
        
        col_t = config.get("coluna_tracking", "")
        if col_t in df.columns:
            resumo = df.groupby(col_t).agg(
                leads=('Score_Total', 'count'),
                score_total=('Score_Total', 'sum'),
                qualificados=('Score_Total', lambda x: (x >= 40).sum())
            ).reset_index()
            st.dataframe(resumo)
        else:
            st.warning("Mapeie a coluna de tracking em 'Conexões'.")
    else:
        st.info("Configure o link do Sheets primeiro.")

# --- OUTRAS PÁGINAS (PRESERVADAS) ---
elif page == "🏠 Dados Consolidados":
    st.title(f"🏠 Dashboard: {projeto_ativo}")
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
