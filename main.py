import streamlit as st
import pandas as pd
import json
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Analytics Pro SaaS", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1f2937; border-radius: 5px; padding: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXÃO COM O BANCO DE DADOS (GSHEETS) ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.sidebar.error("Erro de conexão. Verifique o secrets.toml.")

def carregar_banco():
    try:
        return conn.read(worksheet="Configuracoes", ttl=0)
    except:
        cols = ["Projeto", "Meta_Token", "Meta_ID", "Google_Dev", "Google_CustID", 
                "TikTok_Token", "TikTok_ID", "Hotmart_ID", "Hotmart_Secret", 
                "Kiwify_Token", "Kiwify_ID", "Sheets_URL", "Col_Tracking", "Regras_JSON"]
        return pd.DataFrame(columns=cols)

# --- 3. MENU LATERAL ---
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

# --- 4. FUNÇÕES DE INTELIGÊNCIA ---
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

# --- 5. PÁGINAS ---

if page == "🔌 Conexões":
    st.title("🔌 Configurações de Projetos")
    
    with st.form("form_master"):
        st.subheader(f"⚙️ Configurando: {projeto_ativo}")
        nome_p = st.text_input("Nome do Projeto", value="" if projeto_ativo == "+ Novo Projeto" else projeto_ativo)
        
        tab_t, tab_v, tab_d = st.tabs(["🚀 Plataforma de Captação", "💰 Plataforma de Vendas", "📊 Sheets"])
        
        # Puxando dados existentes para edição
        dados_atuais = df_db[df_db["Projeto"] == projeto_ativo].iloc[0] if projeto_ativo in lista_p else {}

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

        if st.form_submit_button("💾 Salvar Configurações"):
            novo_registro = pd.DataFrame([{
                "Projeto": nome_p, "Meta_Token": m_t, "Meta_ID": m_i, "Google_Dev": g_d,
                "TikTok_Token": t_t, "Hotmart_ID": h_i, "Kiwify_Token": k_t, "Sheets_URL": s_u,
                "Col_Tracking": dados_atuais.get("Col_Tracking", "utm_content"),
                "Regras_JSON": dados_atuais.get("Regras_JSON", "[]")
            }])
            df_final = pd.concat([df_db, novo_registro]).drop_duplicates(subset=['Projeto'], keep='last')
            conn.update(worksheet="Configuracoes", data=df_final)
            st.success("Dados salvos na Planilha Mestra!")
            st.rerun()

elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Inteligência de Leads - {projeto_ativo}")
    if projeto_ativo in lista_p:
        config = df_db[df_db["Projeto"] == projeto_ativo].iloc[0]
        url = config["Sheets_URL"]
        
        if url:
            try:
                df = pd.read_csv(url.replace('/edit#gid=', '/export?format=csv&gid='))
                cols = df.columns.tolist()
                
                # EDITOR DE REGRAS DINÂMICAS
                with st.expander("🛠️ Definir Regras de Pontuação (SaaS Mode)"):
                    c1, c2, c3 = st.columns([2,2,1])
                    col_r = c1.selectbox("Se a coluna...", cols)
                    val_r = c2.text_input("Contiver o texto...")
                    pts_r = c3.number_input("Ganhe pontos", value=10)
                    
                    if st.button("Adicionar Regra"):
                        regras = json.loads(config["Regras_JSON"])
                        regras.append({"coluna": col_r, "valor": val_r, "pontos": pts_r})
                        df_db.loc[df_db["Projeto"] == projeto_ativo, "Regras_JSON"] = json.dumps(regras)
                        conn.update(worksheet="Configuracoes", data=df_db)
                        st.rerun()
                
                # MAPEAMENTO DE UTM
                col_track = st.selectbox("Qual coluna é o seu Traqueamento (UTM)?", cols, 
                                         index=cols.index(config["Col_Tracking"]) if config["Col_Tracking"] in cols else 0)
                if col_track != config["Col_Tracking"]:
                    df_db.loc[df_db["Projeto"] == projeto_ativo, "Col_Tracking"] = col_track
                    conn.update(worksheet="Configuracoes", data=df_db)

                # PROCESSAMENTO
                df_scored = aplicar_scoring(df, config["Regras_JSON"])
                st.subheader("Resultado de Qualidade")
                st.dataframe(df_scored.sort_values(by='Score_Total', ascending=False), use_container_width=True)
            except:
                st.error("Erro ao ler Sheets. Verifique o link em Conexões.")
    else:
        st.info("Selecione um projeto configurado.")

# --- OUTRAS PÁGINAS (PRESERVADAS) ---
elif page == "🏠 Dados Consolidados":
    st.title(f"🏠 Consolidado: {projeto_ativo}")
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
