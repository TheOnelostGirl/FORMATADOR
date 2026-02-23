import streamlit as st
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

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
    para_format.line_spacing = 1.0  # Espaçamento simples
    para_format.left_indent = Cm(4)  # Recuo de 4cm da margem esquerda
    para_format.space_before = Pt(12)
    para_format.space_after = Pt(12)
    
    run = para.add_run(texto)
    run.font.name = 'Arial'
    run.font.size = Pt(10) # Fonte 10 para citação

# --- Interface ---
st.set_page_config(page_title="Formatador ABNT 2.0", layout="centered")

st.title(" Formatador ABNT ")

tipo_texto = st.radio("O que você vai colar agora?", ["Texto Comum (Parágrafos)", "Citação Longa (Mais de 3 linhas)"])
texto_input = st.text_area("Cole aqui:", height=200)

# Usamos o 'session_state' para guardar o que já foi formatado
if 'documento' not in st.session_state:
    st.session_state.documento = Document()
    configurar_margens(st.session_state.documento)
    st.session_state.historico = []

if st.button("Adicionar ao Documento"):
    if texto_input.strip():
        p = st.session_state.documento.add_paragraph()
        if tipo_texto == "Texto Comum (Parágrafos)":
            aplicar_formato_corpo(p, texto_input)
        else:
            aplicar_formato_citacao_longa(p, texto_input)
        
        st.session_state.historico.append(tipo_texto)
        st.success(f"Adicionado como {tipo_texto}!")
    else:
        st.warning("Cole algo antes.")

st.divider()

if st.session_state.historico:
    st.write(f"Itens no documento: {len(st.session_state.historico)}")
    
    # Gerar o arquivo para download
    buffer = io.BytesIO()
    st.session_state.documento.save(buffer)
    buffer.seek(0)
    
    st.download_button(
        label="📥 Baixar Trabalho Completo (.docx)",
        data=buffer,
        file_name="meu_trabalho_abnt.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    if st.button("Limpar e começar novo"):
        st.session_state.documento = Document()
        configurar_margens(st.session_state.documento)
        st.session_state.historico = []
        st.rerun()