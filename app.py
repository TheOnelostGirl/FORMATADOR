import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- CONFIGURAÇÃO DA PÁGINA (Sempre o primeiro comando Streamlit) ---
st.set_page_config(page_title="Formatador da Nico", layout="centered", page_icon="🎓")

# --- FUNÇÕES TÉCNICAS (O "Motor" do app) ---
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

# --- SIDEBAR: APOIO E META DO NOTEBOOK ---
with st.sidebar:
    st.header("🎓 Apoie uma Engenheira")
    
    st.markdown(f"""
    Oi! Eu sou a **Nico**, tenho 25 anos e estou no **9º semestre de Engenharia no IFPA**. 
    
    Criei esse app porque cansei de brigar com a ABNT no meu TCC. Hoje, eu programo em um PC fixo porque meu notebook está com a **tela toda quebrada** (conforme mostrei no vídeo!). 
    
    Minha meta é um notebook novo para levar meus projetos de robótica para o laboratório e finalizar o curso! 💻⚡
    """)

    # --- BARRA DE PROGRESSO ---
    valor_meta = 3500.00
    valor_atual = 150.00 # <--- ATUALIZE MANUALMENTE AQUI QUANDO RECEBER PIX
    progresso = min(valor_atual / valor_meta, 1.0)
    
    st.write(f"**Meta Notebook: R$ {valor_atual:.2f} / R$ {valor_meta:.2f}**")
    st.progress(progresso)
    
    # --- DADOS DE PAGAMENTO ---
    st.info("🔑 **Chave Pix (E-mail ou PicPay):** seu-email@exemplo.com")
    st.caption("Qualquer valor ajuda nos meus exames de saúde e no notebook! 🙏")
    
    st.divider()

    # --- LISTA DE APOIADORES ---
    st.subheader("✨ Apoiadores")
    try:
        # Quando tiver o link do CSV da planilha, cole aqui:
        url_planilha = "COLE_AQUI_O_LINK_DO_CSV" 
        df = pd.read_csv(url_planilha)
        for index, row in df.tail(5).iterrows():
            st.write(f"⭐ {row['Nome']}")
    except:
        st.write("🙏 Apoiadores: Namorada ❤️, Marcos S.") # Coloquei uns nomes de exemplo

# --- INTERFACE PRINCIPAL ---
st.title("🚀 Formatador ABNT Inteligente")
st.write("Facilitando a vida do estudante, um parágrafo por vez.")

tipo_texto = st.radio("O que você vai colar agora?", ["Texto Comum (Parágrafos)", "Citação Longa (Mais de 3 linhas)"])
texto_input = st.text_area("Cole seu texto aqui:", height=200)

# Inicialização do documento no session_state
if 'documento' not in st.session_state:
    st.session_state.documento = Document()
    configurar_margens(st.session_state.documento)
    st.session_state.historico = []

# Botão de Adicionar
if st.button("Adicionar ao Documento"):
    if texto_input.strip():
        p = st.session_state.documento.add_paragraph()
        if tipo_texto == "Texto Comum (Parágrafos)":
            aplicar_formato_corpo(p, texto_input)
        else:
            aplicar_formato_citacao_longa(p, texto_input)
        
        st.session_state.historico.append(tipo_texto)
        st.success(f"Adicionado com sucesso!")
    else:
        st.warning("Opa! Cole o texto antes de clicar.")

st.divider()

# Parte de Download
if st.session_state.historico:
    st.write(f"📝 Itens já formatados: {len(st.session_state.historico)}")
    
    buffer = io.BytesIO()
    st.session_state.documento.save(buffer)
    buffer.seek(0)
    
    st.download_button(
        label="📥 Baixar Trabalho Completo (.docx)",
        data=buffer,
        file_name="trabalho_formatado_nico.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    if st.button("🗑️ Limpar tudo e recomeçar"):
        st.session_state.documento = Document()
        configurar_margens(st.session_state.documento)
        st.session_state.historico = []
        st.rerun() = []
        st.rerun()
