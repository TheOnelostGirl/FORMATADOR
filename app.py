import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Formatador da Nico", layout="centered", page_icon="🎓")

# --- FUNÇÕES TÉCNICAS ---
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

    # INDENTAÇÃO CORRIGIDA: Agora o texto aparece dentro da barra lateral
    st.markdown(f"""
    ### 🛠️ Apoie uma Engenheira em Formação!
    
    Sou a **Nico**, 25 anos, futura Engenheira de Controle e Automação pelo **IFPA** (9º semestre). Desenvolvi este formatador para devolver o tempo que a burocracia da ABNT rouba de nós.
    
    **Por que o seu apoio é imprescindível hoje?**
    Na Engenharia, a inovação não acontece sentada em uma mesa. Ela acontece no laboratório, na bancada de robótica e no campo. Atualmente, meu desenvolvimento está "preso" a um PC fixo, o que é um gargalo crítico na minha reta final de curso.
    
    Ter um notebook funcional não é um luxo, é a **condição básica** para eu levar meus códigos para o laboratório e entregar meu TCC. 
    
    Ao apoiar, você não está apenas fazendo uma doação; você está **investindo no futuro da tecnologia nacional** e ajudando uma estudante a cruzar a linha de chegada.
    
    **Vamos juntos transformar esse projeto em carreira?** 🚀
    """)


    # Adicionando o QR Code
    try:
        st.image("qrcode.png", caption="Escaneie para apoiar a Nico! ☕")
    except:
        st.caption("(QR Code não carregado - verifique o nome do arquivo qrcode.png)")
    
    st.divider()

    # --- LISTA DE APOIADORES ---
    st.subheader("✨")
    try:
        url_planilha = "COLE_AQUI_O_LINK_DO_CSV" 
        df = pd.read_csv(url_planilha)
        for index, row in df.tail(5).iterrows():
            st.write(f"⭐ {row['Nome']}")
    except:
        st.write("Apoiadores: ")

# --- INTERFACE PRINCIPAL ---
st.title(" Formatador ABNT")
st.write("Facilitando a vida do estudante, um parágrafo por vez.")

tipo_texto = st.radio("O que você vai colar agora?", ["Texto Comum (Parágrafos)", "Citação Longa (Mais de 3 lines)"])
texto_input = st.text_area("Cole seu texto aqui:", height=200)

if 'documento' not in st.session_state:
    st.session_state.documento = Document()
    configurar_margens(st.session_state.documento)
    st.session_state.historico = []

if st.button("Adicionar ao Documento"):
    if texto_input.strip():
        p = st.session_state.documento
