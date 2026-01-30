#!/usr/bin/env python
"""Modelos de dados com Pydantic."""

from pydantic import BaseModel, Field
from typing import Optional

class ProjectConfig(BaseModel):
    """Configuração de um projeto."""
    
    Projeto: str
    Meta_Token: Optional[str] = None
    Meta_ID: Optional[str] = None
    Google_Dev: Optional[str] = None
    Google_CustID: Optional[str] = None
    TikTok_Token: Optional[str] = None
    TikTok_ID: Optional[str] = None
    Hotmart_ID: Optional[str] = None
    Hotmart_Secret: Optional[str] = None
    Kiwify_Token: Optional[str] = None
    
    class Config:
        from_attributes = True
