#!/usr/bin/env python
"""
Analytics Pro SaaS - Aplicação Principal

Arquivo principal do Streamlit. Responsável por:
1. Configurar a página
2. Gerenciar a navegação
3. Orquestrar as páginas
"""

import streamlit as st
from config.settings import settings
from src.services.database_service import get_projects_list, get_project_config

# Importar páginas
from pages import (
    dados_consolidados,
    conexoes,
    lead_scoring,
    meta_ads,
    google_ads,
    tiktok_ads,
    hotmart,
    kiwify,
    funil_perpetuo
)

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title=settings.page_title,
    layout=settings.layout,
    initial_sidebar_state=settings.initial_sidebar_state,
)

# --- 2. ESTILO DARK (VK METRICS) ---
st.markdown(settings.theme_vk_metrics, unsafe_allow_html=True)

# --- 3. INICIALIZAR SESSION STATE ---
if 'projeto_ativo' not in st.session_state:
    st.session_state.projeto_ativo = None
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Dados Consolidados"

# --- 4. BARRA LATERAL ---
with st.sidebar:
    st.title("🛡️ Gestão de Tráfego")
    st.caption(f"v{settings.app_version}")
    st.divider()

    # Obter lista de projetos
    projects_list = get_projects_list()
    
    # Seletor de projeto
    projeto_selecionado = st.selectbox(
        "📁 Projeto Ativo",
        projects_list + ["+ Novo Projeto"],
        index=0 if projects_list else 0,
        key="projeto_selector"
    )
    
    # Atualizar projeto ativo
    if projeto_selecionado == "+ Novo Projeto":
        st.session_state.projeto_ativo = None
    else:
        st.session_state.projeto_ativo = projeto_selecionado

    st.divider()

    # Menu de navegação
    st.subheader("📋 Menu")
    
    page = st.radio(
        "Selecione uma página:",
        [
            "🏠 Dados Consolidados",
            "🔌 Conexões",
            "🎯 Lead Scoring",
            "🔵 Meta Ads",
            "🔴 Google Ads",
            "⚫ TikTok Ads",
            "🟠 Hotmart",
            "🟢 Kiwify",
            "🌪️ Funil de Perpétuo"
        ],
        key="page_selector"
    )
    
    st.session_state.page = page

    st.divider()

    # Informações do projeto
    if st.session_state.projeto_ativo:
        st.subheader("📊 Informações do Projeto")
        config = get_project_config(st.session_state.projeto_ativo)
        
        if config:
            col1, col2 = st.columns(2)
            
            with col1:
                if config.Meta_Token:
                    st.success("✅ Meta Ads")
                else:
                    st.warning("⚠️ Meta Ads")
            
            with col2:
                if config.Google_Dev:
                    st.success("✅ Google Ads")
                else:
                    st.warning("⚠️ Google Ads")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if config.TikTok_Token:
                    st.success("✅ TikTok Ads")
                else:
                    st.warning("⚠️ TikTok Ads")
            
            with col2:
                if config.Hotmart_ID:
                    st.success("✅ Hotmart")
                else:
                    st.warning("⚠️ Hotmart")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if config.Kiwify_Token:
                    st.success("✅ Kiwify")
                else:
                    st.warning("⚠️ Kiwify")

# --- 5. RENDERIZAR PÁGINA SELECIONADA ---
if st.session_state.page == "🏠 Dados Consolidados":
    dados_consolidados.render(st.session_state.projeto_ativo)

elif st.session_state.page == "🔌 Conexões":
    conexoes.render(st.session_state.projeto_ativo)

elif st.session_state.page == "🎯 Lead Scoring":
    lead_scoring.render(st.session_state.projeto_ativo)

elif st.session_state.page == "🔵 Meta Ads":
    meta_ads.render(st.session_state.projeto_ativo)

elif st.session_state.page == "🔴 Google Ads":
    google_ads.render(st.session_state.projeto_ativo)

elif st.session_state.page == "⚫ TikTok Ads":
    tiktok_ads.render(st.session_state.projeto_ativo)

elif st.session_state.page == "🟠 Hotmart":
    hotmart.render(st.session_state.projeto_ativo)

elif st.session_state.page == "🟢 Kiwify":
    kiwify.render(st.session_state.projeto_ativo)

elif st.session_state.page == "🌪️ Funil de Perpétuo":
    funil_perpetuo.render(st.session_state.projeto_ativo)
