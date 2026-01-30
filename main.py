# --- FUNÇÃO DO MOTOR DE REGRAS (O CORAÇÃO DO SAAS) ---
def processar_score_dinamico(df, regras, mapeamento):
    df['Score_Total'] = 0
    
    # Aplica cada regra definida pelo usuário
    for regra in regras:
        coluna = regra['coluna']
        valor_chave = regra['valor']
        pontos = regra['pontos']
        
        if coluna in df.columns:
            # Verifica se o valor existe na coluna (sem diferenciar maiúsculas/minúsculas)
            df.loc[df[coluna].astype(str).str.contains(valor_chave, case=False, na=False), 'Score_Total'] += pontos
            
    return df

# --- PÁGINA: LEAD SCORING ---
elif page == "🎯 Lead Scoring":
    st.title(f"🎯 Lead Scoring Dinâmico: {projeto_ativo}")
    
    # Buscamos as configurações que o usuário salvou para este projeto
    config = st.session_state["banco_projetos"].get(projeto_ativo, {})
    coluna_ads = config.get("coluna_tracking", "utm_content") # Padrão é utm_content
    regras_projeto = config.get("regras_score", [])

    url_sheets = st.text_input("Link CSV do Sheets", key=f"url_{projeto_ativo}")

    if url_sheets:
        df_leads = pd.read_csv(url_sheets.replace('/edit#gid=', '/export?format=csv&gid='))
        
        # Processa o score usando as regras customizadas
        df_final = processar_score_dinamico(df_leads, regras_projeto, coluna_ads)
        
        # Cruzamento com Meta Ads usando a coluna de tracking escolhida
        st.subheader("Análise de Qualidade por Anúncio")
        if coluna_ads in df_final.columns:
            relatorio = df_final.groupby(coluna_ads).agg(
                leads=('Score_Total', 'count'),
                score_medio=('Score_Total', 'mean')
            ).reset_index()
            st.dataframe(relatorio)
        else:
            st.error(f"A coluna de traqueamento '{coluna_ads}' não foi encontrada na sua planilha.")

# --- PÁGINA: CONEXÕES (ONDE O USUÁRIO CONFIGURA O SISTEMA) ---
elif page == "🔌 Conexões":
    st.title(f"🔌 Configuração do Projeto: {projeto_ativo}")
    
    # SEÇÃO DE MAPEAMENTO
    st.subheader("1. Mapeamento de Traqueamento")
    col_track = st.text_input("Qual o nome da coluna de UTM no seu Sheets?", value="utm_content")
    
    # SEÇÃO DE REGRAS DE PONTUAÇÃO
    st.subheader("2. Regras de Lead Scoring")
    st.info("Defina quais respostas valem pontos para esse projeto específico.")
    
    # Interface para criar regras dinamicamente
    if "regras_temp" not in st.session_state: st.session_state.regras_temp = []
    
    c1, c2, c3 = st.columns([2, 2, 1])
    nova_col = c1.text_input("Nome da Coluna (ex: Profissão)")
    novo_val = c2.text_input("Valor esperado (ex: Empresário)")
    nova_pt = c3.number_input("Pontos", value=10)
    
    if st.button("➕ Adicionar Regra"):
        st.session_state.regras_temp.append({"coluna": nova_col, "valor": novo_val, "pontos": nova_pt})
        
    st.write("Regras Ativas:", st.session_state.regras_temp)
    
    if st.button("💾 Salvar Configurações"):
        # Salva no banco de dados do projeto
        st.session_state["banco_projetos"][projeto_ativo]["coluna_tracking"] = col_track
        st.session_state["banco_projetos"][projeto_ativo]["regras_score"] = st.session_state.regras_temp
        st.success("Configurações salvas!")
