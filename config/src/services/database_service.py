#!/usr/bin/env python
"""
Serviço de Banco de Dados - Google Sheets

Gerencia a conexão e operações com Google Sheets.
"""

import streamlit as st
import pandas as pd
from typing import Optional, List

@st.cache_resource
def get_connection():
    """Retorna a conexão com Google Sheets."""
    try:
        return st.connection("gsheets", type=GSheetsConnection)
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
    conn = get_connection()
    if conn is None:
        return []
    
    df = load_database(conn)
    if df.empty:
        return []
    
    return df["Projeto"].unique().tolist()

def get_project_config(project_name: str):
    """Retorna configuração do projeto."""
    conn = get_connection()
    if conn is None or not project_name:
        return None
    
    df = load_database(conn)
    if df.empty:
        return None
    
    project = df[df["Projeto"] == project_name]
    if project.empty:
        return None
    
    return project.iloc[0]

def save_project_config(project_name: str, config: dict) -> bool:
    """Salva configuração do projeto."""
    conn = get_connection()
    if conn is None:
        return False
    
    df = load_database(conn)
    
    if project_name in df["Projeto"].values:
        df.loc[df["Projeto"] == project_name] = [project_name] + list(config.values())
    else:
        new_row = pd.DataFrame([[project_name] + list(config.values())], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
    
    try:
        conn.update(worksheet="Configuracoes", data=df)
        st.cache_data.clear()
        return True
    except:
        return False

def delete_project(project_name: str) -> bool:
    """Deleta um projeto."""
    conn = get_connection()
    if conn is None:
        return False
    
    df = load_database(conn)
    df = df[df["Projeto"] != project_name]
    
    try:
        conn.update(worksheet="Configuracoes", data=df)
        st.cache_data.clear()
        return True
    except:
        return False
