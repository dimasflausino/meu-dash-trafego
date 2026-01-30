import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÃO VISUAL (DARK MODE PREMIUM) ---
st.set_page_config(page_title="Consolidado de Vendas - Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    .stPlotlyChart { border: 1px solid #1f2937; border-radius: 15px; }
    </style>
    """, unsafe_allow_stdio=True)

# --- FUNÇÕES DE CONEXÃO (O "Cérebro" das APIs) ---

def get_data_kiwify(api_key):
    # Aqui o código se conecta com a Kiwify futuramente
    # Por enquanto, ele gera um dado simulado para você ver o design
    return {"vendas": 15200.00, "quantidade": 45}

def get_data_hotmart(client_id, secret):
    # Aqui o código se conecta com a Hotmart futuramente
    return {"vendas": 22450.00, "quantidade": 62}

# --- INTERFACE DO USUÁRIO ---
st.title("📊 Gestão Centralizada de Tráfego e Vendas")
st.write("Conectado: **Hotmart** | **Kiwify**")

# Barra lateral para inserir as chaves (sem precisar mexer no código)
with st.sidebar:
    st.header("Configurações de API")
    st.info("Insira suas chaves abaixo para sincronizar")
    kiwify_key = st.text_input("Token Kiwify", type="password")
    hot_id = st.text_input("Client ID Hotmart")
    
# --- PROCESSAMENTO DOS DADOS ---
# Somando as plataformas
vendas_kiwify = get_data_kiwify(kiwify_key)
vendas_hotmart = get_data_hotmart(hot_id, "")

faturamento_total = vendas_kiwify["vendas"] + vendas_hotmart["vendas"]
vendas_totais = vendas_kiwify["quantidade"] + vendas_hotmart["quantidade"]

# --- BLOCO DE KPIs (ESTILO VK METRICS) ---
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Faturamento Acumulado", f"R$ {faturamento_total:,.2f}", delta="15% vs ontem")
with c2:
    st.metric("Total de Vendas", f"{vendas_totais} unid.")
with c3:
    st.metric("Ticket Médio", f"R$ {faturamento_total/vendas_totais:,.2f}")
with c4:
    st.metric("ROI Estimado", "4.2x", delta="0.3x", delta_color="normal")

st.markdown("---")

# --- GRÁFICO DE COMPARAÇÃO DE PLATAFORMAS ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("Faturamento por Origem")
    df_pizza = pd.DataFrame({
        "Plataforma": ["Kiwify", "Hotmart"],
        "Valor": [vendas_kiwify["vendas"], vendas_hotmart["vendas"]]
    })
    fig = px.pie(df_pizza, values='Valor', names='Plataforma', hole=.5, 
                 color_discrete_sequence=['#00ffcc', '#ff4b4b'], template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("Meta Diária de Faturamento")
    # Simulação de progresso
    progresso = 65 
    st.progress(progresso)
    st.write(f"Você atingiu **{progresso}%** da sua meta de R$ 50.000,00")
