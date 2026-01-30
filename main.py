import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Pro", layout="wide")

# --- MENU LATERAL ---
with st.sidebar:
    st.title("🛡️ Painel de Controle")
    page = st.radio("Navegação", ["Visão Geral", "🎯 Lead Scoring", "🌪️ Funil de Perpétuo", "🔌 Conexões"])
    st.divider()
    st.info("Logado como: Usuário Administrador")

# --- FUNÇÃO DE LEAD SCORING (Lógica de Negócio) ---
def calcular_score(df):
    score = 0
    # Exemplo: Se profissão for 'Empresário' ganha 20 pontos
    # Vamos criar uma lógica que você pode ajustar
    df['Score'] = 0
    df.loc[df['Profissão'].str.contains('Empresário', na=False), 'Score'] += 20
    df.loc[df['Faturamento'].str.contains('> 10k', na=False), 'Score'] += 30
    return df

# --- PÁGINA: LEAD SCORING ---
if page == "🎯 Lead Scoring":
    st.title("Inteligência de Leads (Google Sheets)")
    
    # URL da sua planilha (precisa estar pública ou com segredos configurados)
    sheet_url = st.text_input("Link da Planilha de Leads")
    
    if sheet_url:
        # Lendo dados do Sheets
        df_leads = pd.read_csv(sheet_url.replace('/edit#gid=', '/export?format=csv&gid='))
        df_scored = calcular_score(df_leads)
        
        # Filtro de Leads Qualificados
        leads_quentes = df_scored[df_scored['Score'] >= 40]
        
        c1, c2 = st.columns(2)
        c1.metric("Total de Leads", len(df_scored))
        c2.metric("Leads Qualificados (Score > 40)", len(leads_quentes))
        
        st.dataframe(df_scored.sort_values(by='Score', ascending=False))

# --- PÁGINA: FUNIL DE PERPÉTUO ---
elif page == "🌪️ Funil de Perpétuo":
    st.title("Análise de Upsell e Order Bump")
    st.write("Cálculo baseado em produtos separados no checkout.")
    
    # Exemplo de tabela de conversão
    dados_funil = {
        "Etapa": ["Produto Principal", "Order Bump 1", "Upsell 1", "Downsell"],
        "Vendas": [100, 35, 12, 5]
    }
    df_funil = pd.DataFrame(dados_funil)
    
    # Cálculo de % de Anexação (Attach Rate)
    vendas_base = df_funil.iloc[0]['Vendas']
    df_funil['Conversão (%)'] = (df_funil['Vendas'] / vendas_base) * 100
    
    st.table(df_funil)
