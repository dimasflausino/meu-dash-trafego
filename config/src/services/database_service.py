#!/usr/bin/env python
"""
Serviço de Banco de Dados - Google Sheets
"""

import streamlit as st
import pandas as pd
from typing import Optional, List

@st.cache_resource
def get_connection():
    """Retorna a conexão com Google Sheets."""
    try:
        return st.connection("gsheets", type=st.connections.SQLConnection)
    except:
        return None

def load_database(conn) -> pd.DataFrame:
    """Carrega dados do Google Sheets."""
    try:
        df = conn.read(worksheet="Configuracoes", usecols=list(range(20)))
        return df.fillna("")
    except:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_projects_list() -> List[str]:
    """Retorna lista de projetos."""
    try:
        conn = get_connection()
        if conn is None:
            return []
        df = load_database(conn)
        if df.empty or "Projeto" not in df.columns:
            return []
        return df["Projeto"].dropna().unique().tolist()
    except:
        return []

def get_project_config(project_name: str):
    """Retorna configuração do projeto."""
    try:
        if not project_name:
            return None
        conn = get_connection()
        if conn is None:
            return None
        df = load_database(conn)
        if df.empty or "Projeto" not in df.columns:
            return None
        project = df[df["Projeto"] == project_name]
        if project.empty:
            return None
        return project.iloc[0]
    except:
        return None

def save_project_config(project_name: str, config: dict) -> bool:
    """Salva configuração do projeto."""
    try:
        conn = get_connection()
        if conn is None:
            return False
        df = load_database(conn)
        if project_name in df["Projeto"].values:
            df.loc[df["Projeto"] == project_name] = [project_name] + list(config.values())
        else:
            new_row = pd.DataFrame([[project_name] + list(config.values())], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
        conn.update(worksheet="Configuracoes", data=df)
        st.cache_data.clear()
        return True
    except:
        return False

def delete_project(project_name: str) -> bool:
    """Deleta um projeto."""
    try:
        conn = get_connection()
        if conn is None:
            return False
        df = load_database(conn)
        df = df[df["Projeto"] != project_name]
        conn.update(worksheet="Configuracoes", data=df)
        st.cache_data.clear()
        return True
    except:
        return False
