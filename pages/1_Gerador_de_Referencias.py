import streamlit as st
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gerador de Referências", layout="wide", page_icon="📚")

# --- CONTROLE DE SESSÃO ---
if 'contador_ref' not in st.session_state:
    st.session_state.contador_ref = 0
if 'is_vip' not in st.session_state:
    st.session_state.is_vip = False

# --- DIVIDINDO A TELA ---
col_principal, col_apoio = st.columns([7, 3], gap="large")

# ==========================================
# 1. LADO DIREITO: CARREGANDO O APOIO PRIMEIRO
# (Isso garante que o QR Code não suma no bloqueio)
# ==========================================
with col_apoio:
    st.header("🎓 Apoie o Projeto")
    
    try:
        # Certifique-se de que o arquivo qrcode.png está na pasta principal do projeto
        st.image("qrcode.png", caption="✨ Invista na infraestrutura técnica da futura engenheira.")
    except:
        st.info("Espaço para o QR Code (qrcode.png)")
    
    st.success("🔑 Chave Pix: seu-email@exemplo.com")
    st.divider()

    st.markdown("""
    ### 🛠️ Apoie uma Engenheira em Formação!
    
    Sou a **Nico**, 25 anos, futura Engenheira de Controle e Automação pelo **IFPA** (9º semestre). Desenvolvi este formatador para devolver o tempo que a burocracia da ABNT rouba de nós.
    
    **Por que o seu apoio é imprescindível hoje?** Na Engenharia, a inovação não acontece sentada em uma mesa. Ela acontece no laboratório, na bancada de robótica e no campo. Atualmente, meu desenvolvimento está "preso" a um PC fixo, o que é um gargalo crítico na minha reta final de curso.
    
    Ter um notebook funcional não é um luxo, é a **condição básica** para eu levar meus códigos para o laboratório e entregar meu TCC. 
    """)

# ==========================================
# 2. LADO ESQUERDO: GERADOR E TRAVA VIP
# ==========================================
with col_principal:
    st.title("📚 Gerador Automático de Referências")

    # 🛑 A TRAVA VIP (Agora com a lateral já carregada!)
    if st.session_state.contador_ref >= 5 and not st.session_state.is_vip:
        st.error("🛑 Limite de 5 referências gratuitas atingido!")
        st.markdown("""
        **Gostou da ferramenta?** Para liberar o uso ilimitado e apoiar o desenvolvimento do projeto, faça um Pix de **R$ 5,00** (QR Code na lateral). 
        """)
        
        # Substitua SEUDDDENUMERO pelo seu número real
        link_zap = "https://wa.me/5591983270175?text=Oi%20Nico!%20Fiz%20o%20Pix%20para%20liberar%20o%20VIP."
        st.link_button("📱 Enviar comprovante no WhatsApp", link_zap)
        
        senha_digitada = st.text_input(" Digite sua Senha VIP aqui e aperte Enter:")
        
        if senha_digitada == "EuAmoAABNT2026": 
            st.session_state.is_vip = True
            st.success("Acesso VIP Liberado! Atualize a página.")
            st.rerun()
            
        st.stop() # Agora ele para aqui, mas a coluna lateral já "nasceu" lá em cima

    # MENSAGEM DE STATUS
    if st.session_state.is_vip:
        st.success("👑 Modo VIP Ativado: Uso ilimitado liberado!")
    else:
        restantes = 5 - st.session_state.contador_ref
        st.info(f"Você tem {restantes} referência(s) gratuita(s) restante(s).")

    st.divider()

    # --- FORMULÁRIOS ---
    tipo = st.selectbox("Qual tipo de fonte você quer referenciar?", [
        "Livro", 
        "Site / Artigo Online", 
        "Artigo Científico (Automático via DOI) 🚀"
    ])

    if tipo == "Livro":
        # ... (seu código de livro continua igual)
        st.subheader("📖 Referência de Livro")
        c1, c2 = st.columns(2)
        with c1:
            sobrenome = st.text_input("Sobrenome do Autor (ex: SILVA)").upper()
            nome = st.text_input("Nome do Autor (ex: João)")
        with c2:
            titulo = st.text_input("Título do Livro")
            subtitulo = st.text_input("Subtítulo (opcional)")
        if st.button("Gerar Referência ABNT"):
            if sobrenome and nome and titulo:
                st.session_state.contador_ref += 1
                ref = f"{sobrenome}, {nome}. **{titulo}**..."
                st.success("✅ Gerado!")
                st.markdown(f"> {ref}")

    elif tipo == "Artigo Científico (Automático via DOI) 🚀":
        st.subheader("🔬 Busca Automática ")
        doi_input = st.text_input("Número do DOI (ex: 10.1038/s41586-020-2649-2)")

        if st.button("🔍 Buscar e Gerar ABNT"):
            if doi_input.strip():
                try:
                    doi_limpo = doi_input.replace("https://doi.org/", "").strip()
                    url = f"https://api.crossref.org/works/{doi_limpo}"
                    resposta = requests.get(url)
                    if resposta.status_code == 200:
                        dados = resposta.json()['message']
                        
                        # Processando autores
                        autores_lista = [f"{a.get('family','').upper()}, {a.get('given','')}" for a in dados.get('author', [])]
                        autores_abnt = "; ".join(autores_lista) if autores_lista else "AUTOR DESCONHECIDO"
                        
                        titulo_artigo = dados.get('title', [''])[0]
                        nome_revista = dados.get('container-title', [''])[0]
                        ano_artigo = dados['issued']['date-parts'][0][0]
                        
                        ref_doi = f"{autores_abnt}. {titulo_artigo}. **{nome_revista}**, {ano_artigo}. Disponível em: <https://doi.org/{doi_limpo}>."
                        
                        st.session_state.contador_ref += 1
                        st.success("✅ Artigo encontrado!")
                        st.markdown(f"> {ref_doi}")
                    else:
                        st.error("❌ DOI não encontrado.")
                except:
                    st.error("⚠️ Erro na busca.")
