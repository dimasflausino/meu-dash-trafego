#!/usr/bin/env python
"""
Página de Dados Consolidados - Dashboard Principal

Consolida dados de todas as plataformas (Meta Ads, Google Ads, TikTok Ads, Hotmart, Kiwify)
e exibe um dashboard com KPIs, gráficos e análises.

Design baseado no VK Metrics com suporte a temas (Dark, Light, Sistema).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from src.services import meta_ads_service, google_ads_service, tiktok_ads_service, hotmart_service, kiwify_service
from src.services.database_service import get_project_config


# ============================================================================
# CONFIGURAÇÃO DE TEMAS
# ============================================================================

THEMES = {
    "dark": {
        "bg_color": "#0B0E14",
        "text_color": "#FFFFFF",
        "card_bg": "#1F2937",
        "accent_color": "#7C3AED",
        "secondary_color": "#6D28D9",
        "success_color": "#10B981",
        "warning_color": "#F59E0B",
        "danger_color": "#EF4444",
        "grid_color": "#374151",
    },
    "light": {
        "bg_color": "#FFFFFF",
        "text_color": "#1F2937",
        "card_bg": "#F3F4F6",
        "accent_color": "#7C3AED",
        "secondary_color": "#6D28D9",
        "success_color": "#10B981",
        "warning_color": "#F59E0B",
        "danger_color": "#EF4444",
        "grid_color": "#E5E7EB",
    }
}


def get_theme() -> dict:
    """Retorna o tema baseado na preferência do usuário."""
    if 'theme' not in st.session_state:
        st.session_state.theme = "dark"
    return THEMES[st.session_state.theme]


def apply_theme_css(theme: dict):
    """Aplica CSS customizado baseado no tema selecionado."""
    css = f"""
    <style>
        :root {{
            --bg-color: {theme['bg_color']};
            --text-color: {theme['text_color']};
            --card-bg: {theme['card_bg']};
            --accent-color: {theme['accent_color']};
        }}
        
        .main {{
            background-color: {theme['bg_color']};
            color: {theme['text_color']};
        }}
        
        .stMetricValue {{
            font-size: 28px;
            color: {theme['accent_color']};
            font-weight: bold;
        }}
        
        .stMetricLabel {{
            color: {theme['text_color']};
            font-size: 14px;
        }}
        
        .metric-card {{
            background-color: {theme['card_bg']};
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid {theme['accent_color']};
        }}
        
        .stButton > button {{
            background-color: {theme['accent_color']};
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        }}
        
        .stButton > button:hover {{
            background-color: {theme['secondary_color']};
        }}
        
        .stSelectbox, .stDateInput {{
            background-color: {theme['card_bg']};
            color: {theme['text_color']};
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def render(project_name: str):
    """Renderiza a página de dados consolidados."""
    
    # Aplicar tema
    theme = get_theme()
    apply_theme_css(theme)
    
    # --- HEADER COM SELETOR DE TEMA ---
    col1, col2 = st.columns([0.9, 0.1])
    
    with col1:
        st.title("📊 Dashboard Consolidado")
    
    with col2:
        theme_option = st.selectbox(
            "Tema",
            ["dark", "light"],
            index=0 if st.session_state.theme == "dark" else 1,
            key="theme_selector"
        )
        if theme_option != st.session_state.theme:
            st.session_state.theme = theme_option
            st.rerun()
    
    # --- VERIFICAÇÕES INICIAIS ---
    if not project_name:
        st.warning("⚠️ Selecione um projeto na barra lateral para visualizar os dados.")
        return

    config = get_project_config(project_name)
    if not config:
        st.error(f"❌ Não foi possível carregar a configuração para o projeto '{project_name}'.")
        return

    # --- FILTROS DE DATA ---
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.date_input(
            "📅 Período",
            (datetime.now() - timedelta(days=7), datetime.now()),
            format="DD/MM/YYYY"
        )
    
    with col2:
        if st.button("🔄 Atualizar Dados"):
            st.cache_data.clear()
            st.rerun()
    
    with col3:
        st.info(f"Projeto: **{project_name}**")

    # Garantir que temos um início e fim de data
    if len(date_range) != 2:
        st.warning("Por favor, selecione um período de início e fim.")
        return

    start_date, end_date = date_range

    # --- COLETA DE DADOS (SIMULADOS) ---
    all_data = []
    platforms_enabled = []
    
    if config.Meta_Token:
        meta_df = meta_ads_service.get_meta_performance(start_date, end_date, config.Meta_Token, config.Meta_ID)
        all_data.append(meta_df)
        platforms_enabled.append("Meta Ads")

    if config.Google_Dev:
        google_df = google_ads_service.get_google_performance(start_date, end_date, config.Google_Dev, config.Google_CustID)
        all_data.append(google_df)
        platforms_enabled.append("Google Ads")

    if config.TikTok_Token:
        tiktok_df = tiktok_ads_service.get_tiktok_performance(start_date, end_date, config.TikTok_Token, config.TikTok_ID)
        all_data.append(tiktok_df)
        platforms_enabled.append("TikTok Ads")
        
    if config.Hotmart_ID:
        hotmart_df = hotmart_service.get_hotmart_sales(start_date, end_date, config.Hotmart_ID, config.Hotmart_Secret)
        all_data.append(hotmart_df)
        platforms_enabled.append("Hotmart")

    if config.Kiwify_Token:
        kiwify_df = kiwify_service.get_kiwify_sales(start_date, end_date, config.Kiwify_Token)
        all_data.append(kiwify_df)
        platforms_enabled.append("Kiwify")

    if not all_data:
        st.info("ℹ️ Nenhuma plataforma de dados configurada. Vá em '🔌 Conexões' para configurar.")
        return

    # --- CONSOLIDAÇÃO DOS DADOS ---
    df_consolidado = pd.concat(all_data, ignore_index=True).fillna(0)

    # --- CÁLCULO DAS MÉTRICAS ---
    total_investment = df_consolidado.get('investment', pd.Series(0)).sum()
    total_revenue = df_consolidado.get('revenue', pd.Series(0)).sum()
    total_sales = df_consolidado.get('sales', pd.Series(0)).sum()
    net_profit = total_revenue - total_investment
    roi = (net_profit / total_investment * 100) if total_investment > 0 else 0

    # --- EXIBIÇÃO DOS KPIs (ESTILO VK METRICS) ---
    st.subheader("📈 KPIs Principais")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.metric(
            "💰 Investimento Total",
            f"R$ {total_investment:,.2f}",
            delta=f"{len(platforms_enabled)} plataformas"
        )
    
    with kpi_col2:
        st.metric(
            "📊 Faturamento Total",
            f"R$ {total_revenue:,.2f}",
            delta=f"+{((total_revenue / total_investment - 1) * 100):.1f}%" if total_investment > 0 else "N/A"
        )
    
    with kpi_col3:
        st.metric(
            "💸 Lucro Líquido",
            f"R$ {net_profit:,.2f}",
            delta="✅ Positivo" if net_profit > 0 else "❌ Negativo"
        )
    
    with kpi_col4:
        st.metric(
            "💹 ROI",
            f"{roi:.2f}%",
            delta="Retorno sobre investimento"
        )

    st.divider()

    # --- GRÁFICOS ---
    st.subheader("📉 Análises Visuais")
    
    # Preparar dados para gráficos
    df_grouped_date = df_consolidado.groupby('date')[['revenue', 'investment']].sum().reset_index()
    df_grouped_platform = df_consolidado.groupby('platform')['revenue'].sum().reset_index()
    
    # Gráfico 1: Faturamento vs Investimento por Dia (Linha + Barras)
    fig_daily = go.Figure()
    
    fig_daily.add_trace(go.Bar(
        x=df_grouped_date['date'],
        y=df_grouped_date['investment'],
        name='Investimento',
        marker_color=theme['accent_color'],
        opacity=0.7
    ))
    
    fig_daily.add_trace(go.Scatter(
        x=df_grouped_date['date'],
        y=df_grouped_date['revenue'],
        name='Faturamento',
        mode='lines+markers',
        line=dict(color=theme['success_color'], width=3),
        marker=dict(size=8)
    ))
    
    fig_daily.update_layout(
        title="Faturamento vs Investimento por Dia",
        xaxis_title="Data",
        yaxis_title="Valor (R$)",
        hovermode='x unified',
        template="plotly_dark" if st.session_state.theme == "dark" else "plotly",
        plot_bgcolor=theme['card_bg'],
        paper_bgcolor=theme['bg_color'],
        font=dict(color=theme['text_color']),
        height=400
    )
    
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # Gráfico 2: Distribuição por Plataforma (Pizza)
    col1, col2 = st.columns(2)
    
    with col1:
        fig_platform = px.pie(
            df_grouped_platform,
            values='revenue',
            names='platform',
            title='Distribuição de Faturamento por Plataforma',
            color_discrete_sequence=[theme['accent_color'], theme['secondary_color'], theme['success_color'], theme['warning_color'], theme['danger_color']]
        )
        
        fig_platform.update_layout(
            template="plotly_dark" if st.session_state.theme == "dark" else "plotly",
            paper_bgcolor=theme['bg_color'],
            font=dict(color=theme['text_color']),
            height=400
        )
        
        st.plotly_chart(fig_platform, use_container_width=True)
    
    with col2:
        # Gráfico 3: Resumo por Plataforma (Barras Horizontais)
        fig_platform_bars = px.bar(
            df_grouped_platform.sort_values('revenue', ascending=True),
            y='platform',
            x='revenue',
            orientation='h',
            title='Faturamento por Plataforma',
            labels={'revenue': 'Faturamento (R$)', 'platform': 'Plataforma'},
            color='revenue',
            color_continuous_scale=['#EF4444', '#F59E0B', '#10B981']
        )
        
        fig_platform_bars.update_layout(
            template="plotly_dark" if st.session_state.theme == "dark" else "plotly",
            paper_bgcolor=theme['bg_color'],
            font=dict(color=theme['text_color']),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_platform_bars, use_container_width=True)

    st.divider()

    # --- TABELA DE DADOS CONSOLIDADOS ---
    st.subheader("📋 Dados Consolidados")
    
    with st.expander("Ver dados brutos", expanded=False):
        # Formatar a tabela para exibição
        df_display = df_consolidado.copy()
        df_display['date'] = pd.to_datetime(df_display['date']).dt.strftime('%d/%m/%Y')
        df_display['investment'] = df_display['investment'].apply(lambda x: f"R$ {x:,.2f}")
        df_display['revenue'] = df_display['revenue'].apply(lambda x: f"R$ {x:,.2f}")
        
        st.dataframe(df_display, use_container_width=True)
        
        # Botão de download
        csv = df_consolidado.to_csv(index=False)
        st.download_button(
            label="📥 Baixar dados em CSV",
            data=csv,
            file_name=f"dados_consolidados_{start_date}_{end_date}.csv",
            mime="text/csv"
        )

    st.divider()

    # --- RESUMO DE PLATAFORMAS ATIVAS ---
    st.subheader("🔌 Plataformas Ativas")
    
    cols = st.columns(len(platforms_enabled))
    for idx, platform in enumerate(platforms_enabled):
        with cols[idx]:
            st.info(f"✅ {platform}")
