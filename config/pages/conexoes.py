#!/usr/bin/env python
"""Página de Conexões - Configuração de Tokens."""

import streamlit as st
from src.services.database_service import get_project_config, save_project_config, delete_project
from src.models.schemas import ProjectConfig

def render(project_name: str):
    """Renderiza a página de conexões."""
    
    st.title("🔌 Conexões - Configurar Tokens")
    
    st.divider()
    
    # Seção de Novo Projeto
    st.subheader("📁 Novo Projeto")
    
    novo_projeto = st.text_input("Nome do Projeto", key="novo_projeto_input")
    
    if st.button("Criar Projeto", key="criar_projeto_btn"):
        if novo_projeto:
            config = ProjectConfig(Projeto=novo_projeto)
            if save_project_config(config):
                st.success(f"✅ Projeto '{novo_projeto}' criado com sucesso!")
                st.rerun()
            else:
                st.error("❌ Erro ao criar projeto")
        else:
            st.warning("⚠️ Digite um nome para o projeto")
    
    st.divider()
    
    # Seção de Configuração de Tokens
    if project_name:
        st.subheader(f"🔑 Tokens - {project_name}")
        
        config = get_project_config(project_name)
        
        with st.form(key="tokens_form"):
            st.write("**Meta Ads**")
            meta_token = st.text_input("Meta Token", value=config.Meta_Token or "", type="password", key="meta_token_input")
            meta_id = st.text_input("Meta Account ID", value=config.Meta_ID or "", key="meta_id_input")
            
            st.write("**Google Ads**")
            google_dev = st.text_input("Google Developer Token", value=config.Google_Dev or "", type="password", key="google_dev_input")
            google_cust = st.text_input("Google Customer ID", value=config.Google_CustID or "", key="google_cust_input")
            
            st.write("**TikTok Ads**")
            tiktok_token = st.text_input("TikTok Token", value=config.TikTok_Token or "", type="password", key="tiktok_token_input")
            tiktok_id = st.text_input("TikTok Advertiser ID", value=config.TikTok_ID or "", key="tiktok_id_input")
            
            st.write("**Hotmart**")
            hotmart_id = st.text_input("Hotmart User Code", value=config.Hotmart_ID or "", key="hotmart_id_input")
            hotmart_secret = st.text_input("Hotmart API Token", value=config.Hotmart_Secret or "", type="password", key="hotmart_secret_input")
            
            st.write("**Kiwify**")
            kiwify_token = st.text_input("Kiwify API Token", value=config.Kiwify_Token or "", type="password", key="kiwify_token_input")
            
            if st.form_submit_button("💾 Salvar Configurações"):
                config = ProjectConfig(
                    Projeto=project_name,
                    Meta_Token=meta_token or None,
                    Meta_ID=meta_id or None,
                    Google_Dev=google_dev or None,
                    Google_CustID=google_cust or None,
                    TikTok_Token=tiktok_token or None,
                    TikTok_ID=tiktok_id or None,
                    Hotmart_ID=hotmart_id or None,
                    Hotmart_Secret=hotmart_secret or None,
                    Kiwify_Token=kiwify_token or None
                )
                
                if save_project_config(config):
                    st.success("✅ Configurações salvas com sucesso!")
                else:
                    st.error("❌ Erro ao salvar configurações")
        
        st.divider()
        
        # Seção de Deletar Projeto
        st.subheader("🗑️ Deletar Projeto")
        
        if st.button("Deletar Projeto", key="delete_projeto_btn"):
            if delete_project(project_name):
                st.success(f"✅ Projeto '{project_name}' deletado com sucesso!")
                st.rerun()
            else:
                st.error("❌ Erro ao deletar projeto")
    else:
        st.info("ℹ️ Selecione um projeto na barra lateral para configurar os tokens.")
