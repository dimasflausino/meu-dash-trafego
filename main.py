import streamlit as st
import pandas as pd
import json

# --- FUNÇÃO DE CÁLCULO SAAS (ESCALÁVEL) ---
def processar_score_pro(df, regras_json):
    """Aplica regras de pontuação dinâmicas vindas de um JSON"""
    df['Score_Total'] = 0
    try:
        regras = json.loads(regras_json) if isinstance(regras_json, str) else regras_json
        for r in regras:
            col, val, pts = r['coluna'], r['valor'], r['pontos']
            if col in df.columns:
                # O uso de .str.contains garante que pegamos variações (ex: "Empresário" e "Sou empresário")
                df.loc[df[col].astype(str).str.contains(val, case=False, na=False), 'Score_Total'] += pts
    except Exception as e:
        st.error(f"Erro no processamento de regras: {e}")
    return df

# --- DENTRO DA PÁGINA DE CONEXÕES ---
elif page == "🔌 Conexões":
    st.title("🔌 Configurações de Escala")
    
    # ... (código anterior de tokens de API) ...

    st.subheader("🎯 Configuração de Lead Scoring (SaaS Mode)")
    
    # 1. Carregar Preview das colunas para o usuário escolher
    url_leads = st.text_input("Link CSV do Sheets (Leads)", key="url_leads_saas")
    
    if url_leads:
        try:
            df_preview = pd.read_csv(url_leads.replace('/edit#gid=', '/export?format=csv&gid='))
            colunas_disponiveis = df_preview.columns.tolist()
            
            # 2. Interface de Criação de Regras
            with st.expander("🛠️ Editor de Regras de Pontuação", expanded=True):
                if "regras_list" not in st.session_state:
                    st.session_state.regras_list = []

                c1, c2, c3 = st.columns([2, 2, 1])
                col_regra = c1.selectbox("Se a coluna...", colunas_disponiveis)
                val_regra = c2.text_input("Contiver o texto...", placeholder="Ex: Empresário")
                pts_regra = c3.number_input("Pontos", value=10, step=5)

                if st.button("➕ Adicionar Regra ao Projeto"):
                    nova_regra = {"coluna": col_regra, "valor": val_regra, "pontos": pts_regra}
                    st.session_state.regras_list.append(nova_regra)
                    st.success("Regra adicionada à lista!")

                # Exibir regras atuais com opção de limpar
                st.write("**Regras Ativas:**")
                st.json(st.session_state.regras_list)
                
                if st.button("🗑️ Limpar Todas as Regras"):
                    st.session_state.regras_list = []
                    st.rerun()

            # 3. Mapeamento de Tracking (UTM)
            col_tracking = st.selectbox("Qual coluna identifica o Anúncio (UTM)?", colunas_disponiveis)

            # BOTÃO DE SALVAMENTO FINAL NO BANCO DE DADOS
            if st.button("💾 Salvar Configurações de Inteligência"):
                # Aqui transformamos a lista de regras em texto (JSON) para salvar no Sheets
                regras_formatadas = json.dumps(st.session_state.regras_list)
                
                # Lógica para salvar no seu Sheets Mestre (conn.update)
                st.success("Configuração de SaaS salva com sucesso!")

        except Exception as e:
            st.error("Erro ao conectar com a planilha. Verifique o compartilhamento.")
