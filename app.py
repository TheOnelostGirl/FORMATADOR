import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Formatador da Nico", layout="centered", page_icon="🎓")

# --- FUNÇÕES TÉCNICAS (Regras ABNT) ---
def configurar_margens(doc):
    for section in doc.sections:
        section.top_margin = Cm(3)
        section.left_margin = Cm(3)
        section.right_margin = Cm(2)
        section.bottom_margin = Cm(2)

def aplicar_formato_corpo(para, texto):
    para_format = para.paragraph_format
    para_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    para_format.line_spacing = 1.5
    para_format.first_line_indent = Cm(1.25)
    
    run = para.add_run(texto)
    run.font.name = 'Arial'
    run.font.size = Pt(12)

def aplicar_formato_citacao_longa(para, texto):
    para_format = para.paragraph_format
    para_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    para_format.line_spacing = 1.0
    para_format.left_indent = Cm(4)
    para_format.space_before = Pt(12)
    para_format.space_after = Pt(12)
    
    run = para.add_run(texto)
    run.font.name = 'Arial'
    run.font.size = Pt(10)

# --- SIDEBAR: REORGANIZADA (QR CODE NO TOPO) ---
with st.sidebar:
    st.header("🎓 Apoie o Projeto")
    
    # 1. QR CODE E PIX (IMPACTO IMEDIATO)
    try:
        st.image("qrcode.png")
        st.caption("✨ Invista na infraestrutura técnica e saúde visual da futura engenheira.")
    except:
        st.error("⚠️ QR Code (qrcode.png) não encontrado.")
    
    st.info("🔑 Chave Pix: seu-email@exemplo.com")

    # 2. BARRA DE PROGRESSO
    valor_meta = 3500.00
    valor_atual = 0.00  # <--- Atualize aqui conforme as doações chegarem
    progresso = min(valor_atual / valor_meta, 1.0)
    
    st.write(f"**Meta Notebook: R$ {valor_atual:.2f} / R$ {valor_meta:.2f}**")
    st.progress(progresso)
    
    st.divider()

    # 3. TEXTO DE EXPLICAÇÃO (PERSUASIVO)
    st.markdown("""
    ### 🛠️ Apoie uma Engenheira em Formação!
    
    Sou a **Nico**, 25 anos, futura Engenheira de Controle e Automação pelo **IFPA** (9º semestre). Desenvolvi este formatador para devolver o tempo que a burocracia da ABNT rou
    configurar_margens(st.session_state.documento)
    st.session_state.historico = []

if st.button("Adicionar ao Documento"):
    if texto_input.strip():
        p = st.session_state.documento
