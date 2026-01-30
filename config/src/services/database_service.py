#!/usr/bin/env python
"""Serviço de banco de dados com Google Sheets."""

import streamlit as st
import pandas as pd
from src.models.schemas import ProjectConfig

@st.cache_resource
def get_connection():
    """Obtém conexão com Google Sheets."""
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except:
        return None

@st.cache_data(ttl=300)
def load_database(conn) -> pd.DataFrame:
    """Carrega dados do Google Sheets."""
    try:
        df = conn.read(worksheet="Configuracoes", usecols=list(range(10)))
        return df.fillna("")
    except:
        return pd.DataFrame()

def get_projects_list() -> list:
    """Retorna lista de projetos."""
    conn = get_connection()
    if conn is None:
        return []
    
    df = load_database(conn)
    if df.empty:
        return []
    
    return df["Projeto"].unique().tolist()

def get_project_config(project_name: str) -> ProjectConfig:
    """Obtém configuração de um projeto."""
    if not project_name:
        return None
    
    conn = get_connection()
    if conn is None:
        return None
    
    df = load_database(conn)
    if df.empty:
        return None
    
    project_row = df[df["Projeto"] == project_name]
    if project_row.empty:
        return None
    
    try:
        return ProjectConfig(**project_row.iloc[0].to_dict())
    except:
        return None

def save_project_config(config: ProjectConfig) -> bool:
    """Salva configuração de um projeto."""
    conn = get_connection()
    if conn is None:
        st.error("Não foi possível conectar ao Google Sheets")
        return False
    
    df = load_database(conn)
    
    try:
        existing = df[df["Projeto"] == config.Projeto]
        
        if not existing.empty:
            df.loc[df["Projeto"] == config.Projeto] = config.dict()
        else:
            df = pd.concat([df, pd.DataFrame([config.dict()])], ignore_index=True)
        
        conn.update(worksheet="Configuracoes", data=df)
        st.cache_data.clear()
        st.cache_resource.clear()
        
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

def delete_project(project_name: str) -> bool:
    """Deleta um projeto."""
    conn = get_connection()
    if conn is None:
        st.error("Não foi possível conectar ao Google Sheets")
        return False
    
    df = load_database(conn)
    
    try:
        df = df[df["Projeto"] != project_name]
        conn.update(worksheet="Configuracoes", data=df)
        st.cache_data.clear()
        st.cache_resource.clear()
        
        return True
    except Exception as e:
        st.error(f"Erro ao deletar: {e}")
        return False
