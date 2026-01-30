import streamlit as st

# --- SISTEMA DE NAVEGAÇÃO ---
st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para:", ["🏠 Visão Geral", "🎯 Lead Scoring", "🌪️ Funil de Perpétuo", "⚙️ Configurações"])

if page == "🏠 Visão Geral":
    st.title("Consolidado de Tráfego")
    # Aqui entra o código que já fizemos de gráficos e KPIs

elif page == "🎯 Lead Scoring":
    st.title("Inteligência de Leads")
    st.write("Analise a qualidade dos seus leads por profissão e resposta.")
    # Aqui criaremos a tabela que filtra: Profissão == "Dono de Empresa"

elif page == "🌪️ Funil de Perpétuo":
    st.title("Métricas de Checkout")
    # Colunas para Order Bump, Upsell e Downsell
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Taxa de Order Bump", "28%", delta="3%")
    with c2:
        st.metric("Taxa de Upsell 1", "12%", delta="-1%")

elif page == "⚙️ Configurações":
    st.title("Conexões de API")
    # Onde você coloca os tokens da Kiwify, Facebook, etc.
