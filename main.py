import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Analytics Pro - Qualidade de Ads", layout="wide")

# --- NAVEGAÇÃO ---
page = st.sidebar.radio("Navegação", ["Visão Geral", "🎯 Qualidade por Ad (Meta+Sheets)", "⚙️ Configurações"])

# --- FUNÇÃO DE CÁLCULO DE SCORE ---
def processar_leads(df):
    # Lógica de Score (Ajuste os nomes das colunas conforme seu Sheets)
    df['Score'] = 0
    # Exemplo: +20 pontos para Empresários
    df.loc[df['Profissão'].str.contains('Empresário', na=False, case=False), 'Score'] += 20
    # Exemplo: +30 pontos para faturamento alto
    df.loc[df['Faturamento'].str.contains('> 10k', na=False), 'Score'] += 30
    
    df['Qualificado'] = df['Score'] >= 40
    return df

if page == "🎯 Qualidade por Ad (Meta+Sheets)":
    st.title("Análise de Performance por Qualidade")
    
    # 1. Simulação de Dados do Meta Ads (Onde virá da API)
    # Aqui teremos: Nome do Ad e quanto ele gastou
    meta_data = pd.DataFrame({
        'ad_name': ['Ad_01_Video_Criativo', 'Ad_02_Foto_Depoimento', 'Ad_03_Direto_Venda'],
        'custo': [500.00, 350.00, 800.00]
    })

    # 2. Entrada do Google Sheets
    sheet_url = st.text_input("Link da Planilha de Leads (CSV)", placeholder="Cole o link do seu Sheets aqui...")

    if sheet_url:
        try:
            # Carrega e processa leads
            df_leads = pd.read_csv(sheet_url.replace('/edit#gid=', '/export?format=csv&gid='))
            df_scored = processar_leads(df_leads)

            # 3. Cruzamento (Merge) usando a UTM
            # 'utm_content' ou 'utm_name' deve ser a coluna no seu Sheets
            resumo_leads = df_scored.groupby('utm_ad_name').agg(
                leads_totais=('Email', 'count'),
                leads_qualificados=('Qualificado', 'sum')
            ).reset_index()

            # Junta com os custos do Meta
            df_final = pd.merge(meta_data, resumo_leads, left_on='ad_name', right_on='utm_ad_name', how='left')
            
            # 4. Cálculos de Performance Real
            df_final['CPL_Total'] = df_final['custo'] / df_final['leads_totais']
            df_final['CPL_Qualificado'] = df_final['custo'] / df_final['leads_qualificados']

            # Exibição
            st.subheader("Ranking de Anúncios por Qualidade")
            
            # Colorindo quem está performando bem
            st.dataframe(df_final.style.format({
                'custo': 'R$ {:.2f}',
                'CPL_Total': 'R$ {:.2f}',
                'CPL_Qualificado': 'R$ {:.2f}'
            }).background_gradient(subset=['leads_qualificados'], cmap='Greens'))

            # Insights
            melhor_ad = df_final.loc[df_final['leads_qualificados'].idxmax()]
            st.success(f"🔥 O anúncio **{melhor_ad['ad_name']}** é o campeão em qualidade com {melhor_ad['leads_qualificados']} leads quentes!")

        except Exception as e:
            st.error(f"Erro ao ler planilha: Verifique se os nomes das colunas (Email, Profissão, utm_ad_name) estão corretos.")
