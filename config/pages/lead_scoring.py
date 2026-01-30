#!/usr/bin/env python
"""
Página de Lead Scoring.

Permite criar regras de pontuação dinâmicas para qualificar leads
com base em critérios configuráveis.
"""

import streamlit as st
import pandas as pd
import json
from src.services.database_service import get_project_config, save_project_config
from src.models.schemas import ProjectConfig

def render(project_name: str):
    """Renderiza a página de Lead Scoring."""
    
    st.title(f"🎯 Lead Scoring Dinâmico - {project_name or 'Novo Projeto'}")

    if not project_name:
        st.warning("⚠️ Selecione um projeto na barra lateral para configurar o Lead Scoring.")
        return

    config = get_project_config(project_name)
    if not config:
        st.error(f"❌ Não foi possível carregar a configuração para o projeto '{project_name}'.")
        return

    # --- INICIALIZAR REGRAS NO SESSION STATE ---
    if 'lead_scoring_rules' not in st.session_state:
        # Carrega as regras do JSON armazenado no Google Sheets
        if hasattr(config, 'Regras_JSON') and config.Regras_JSON:
            try:
                st.session_state.lead_scoring_rules = json.loads(config.Regras_JSON)
            except:
                st.session_state.lead_scoring_rules = []
        else:
            st.session_state.lead_scoring_rules = []

    # --- ABAS ---
    tab1, tab2, tab3 = st.tabs(["➕ Criar Regra", "📋 Regras Ativas", "📊 Analisar Leads"])

    # --- ABA 1: CRIAR REGRA ---
    with tab1:
        st.subheader("Criar Nova Regra de Pontuação")
        
        with st.form("form_nova_regra"):
            col1, col2 = st.columns(2)
            
            with col1:
                coluna = st.text_input("Nome da Coluna", placeholder="ex: utm_source, email_domain")
                valor = st.text_input("Valor a Buscar", placeholder="ex: facebook, gmail.com")
            
            with col2:
                pontos = st.number_input("Pontos", min_value=1, max_value=100, value=10)
                operador = st.selectbox("Operador", ["equals", "contains", "startswith"])
            
            if st.form_submit_button("💾 Adicionar Regra"):
                if coluna and valor:
                    nova_regra = {
                        "id": len(st.session_state.lead_scoring_rules) + 1,
                        "coluna": coluna,
                        "valor": valor,
                        "pontos": pontos,
                        "operador": operador
                    }
                    st.session_state.lead_scoring_rules.append(nova_regra)
                    
                    # Salva as regras no Google Sheets
                    config.Regras_JSON = json.dumps(st.session_state.lead_scoring_rules)
                    save_project_config(config)
                    
                    st.success("✅ Regra adicionada com sucesso!")
                else:
                    st.warning("⚠️ Preencha todos os campos.")

    # --- ABA 2: REGRAS ATIVAS ---
    with tab2:
        st.subheader("Regras Ativas")
        
        if not st.session_state.lead_scoring_rules:
            st.info("Nenhuma regra criada ainda. Crie uma na aba anterior.")
        else:
            for idx, regra in enumerate(st.session_state.lead_scoring_rules):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"""
                    **{regra['coluna']}** `{regra['operador']}` **{regra['valor']}** → **+{regra['pontos']} pontos**
                    """)
                
                with col2:
                    if st.button("✏️", key=f"edit_{idx}"):
                        st.info("Edição de regras em desenvolvimento.")
                
                with col3:
                    if st.button("🗑️", key=f"delete_{idx}"):
                        st.session_state.lead_scoring_rules.pop(idx)
                        config.Regras_JSON = json.dumps(st.session_state.lead_scoring_rules)
                        save_project_config(config)
                        st.success("✅ Regra deletada!")
                        st.rerun()

    # --- ABA 3: ANALISAR LEADS ---
    with tab3:
        st.subheader("Analisar e Pontuar Leads")
        
        uploaded_file = st.file_uploader("Carregue um arquivo CSV com seus leads", type=["csv"])
        
        if uploaded_file:
            df_leads = pd.read_csv(uploaded_file)
            
            st.write(f"**Arquivo carregado**: {len(df_leads)} leads encontrados")
            st.dataframe(df_leads.head())
            
            if st.button("🎯 Pontuar Leads"):
                # Aplica as regras aos leads
                df_leads['lead_score'] = 0
                
                for idx, lead in df_leads.iterrows():
                    score = 0
                    for regra in st.session_state.lead_scoring_rules:
                        coluna = regra['coluna']
                        
                        if coluna in df_leads.columns:
                            valor_lead = str(df_leads.loc[idx, coluna]).lower()
                            valor_regra = regra['valor'].lower()
                            
                            if regra['operador'] == 'equals' and valor_lead == valor_regra:
                                score += regra['pontos']
                            elif regra['operador'] == 'contains' and valor_regra in valor_lead:
                                score += regra['pontos']
                            elif regra['operador'] == 'startswith' and valor_lead.startswith(valor_regra):
                                score += regra['pontos']
                    
                    df_leads.loc[idx, 'lead_score'] = score
                
                # Exibe os resultados
                st.success("✅ Leads pontuados!")
                st.dataframe(df_leads.sort_values('lead_score', ascending=False))
                
                # Download dos resultados
                csv = df_leads.to_csv(index=False)
                st.download_button(
                    label="📥 Baixar Leads Pontuados",
                    data=csv,
                    file_name="leads_pontuados.csv",
                    mime="text/csv"
                )

