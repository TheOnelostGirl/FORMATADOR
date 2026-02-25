import streamlit as st
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gerador de Referências", layout="wide", page_icon="📚")

# --- CONTROLE DE SESSÃO (A Mágica do Paywall VIP) ---
if 'contador_ref' not in st.session_state:
    st.session_state.contador_ref = 0
if 'is_vip' not in st.session_state:
    st.session_state.is_vip = False

# --- DIVIDINDO A TELA ---
col_principal, col_apoio = st.columns([7, 3], gap="large")

# ==========================================
# LADO ESQUERDO: GERADOR DE REFERÊNCIAS
# ==========================================
with col_principal:
    st.title("📚 Gerador Automático de Referências")

    # 🛑 A TRAVA VIP
    if st.session_state.contador_ref >= 5 and not st.session_state.is_vip:
        st.error("🛑 Limite de 5 referências gratuitas atingido!")
        st.markdown("""
        **Gostou da ferramenta?** Para liberar o uso ilimitado e apoiar o desenvolvimento do projeto, faça um Pix de **R$ 5,00** (QR Code na lateral). 
        """)
        
        # --- BOTÃO DO WHATSAPP ---
        link_zap = "https://wa.me/55SEUDDDENUMERO?text=Oi%20Nico!%20Fiz%20o%20Pix%20para%20liberar%20o%20VIP%20das%20referências."
        st.link_button("📱 Enviar comprovante no WhatsApp", link_zap)
        
        st.markdown("Depois de enviar o comprovante, insira a senha que eu te passar abaixo:")
        senha_digitada = st.text_input("🔑 Digite sua Senha VIP aqui e aperte Enter:")
        
        if senha_digitada == "IFPA2026": 
            st.session_state.is_vip = True
            st.success("Acesso VIP Liberado! Muito obrigada por apoiar o projeto. Atualize a página.")
            st.rerun()
            
        st.stop() # Esconde os formulários

    # MENSAGEM DE STATUS
    if st.session_state.is_vip:
        st.success("👑 Modo VIP Ativado: Uso ilimitado liberado!")
    else:
        restantes = 5 - st.session_state.contador_ref
        st.info(f"Você tem {restantes} referência(s) gratuita(s) restante(s).")

    st.divider()

    # --- FORMULÁRIOS DE REFERÊNCIA ---
    tipo = st.selectbox("Qual tipo de fonte você quer referenciar?", [
        "Livro", 
        "Site / Artigo Online", 
        "Artigo Científico (Automático via DOI) 🚀"
    ])

    if tipo == "Livro":
        st.subheader("📖 Referência de Livro")
        c1, c2 = st.columns(2)
        with c1:
            sobrenome = st.text_input("Sobrenome do Autor (ex: SILVA)").upper()
            nome = st.text_input("Nome do Autor (ex: João)")
        with c2:
            titulo = st.text_input("Título do Livro (ex: Engenharia Moderna)")
            subtitulo = st.text_input("Subtítulo (opcional)")
        
        c3, c4, c5 = st.columns(3)
        with c3:
            cidade = st.text_input("Cidade (ex: São Paulo)")
        with c4:
            editora = st.text_input("Editora (ex: Atlas)")
        with c5:
            ano = st.text_input("Ano (ex: 2023)")

        if st.button("Gerar Referência ABNT"):
            if sobrenome and nome and titulo and cidade and editora and ano:
                st.session_state.contador_ref += 1 
                if subtitulo:
                    ref = f"{sobrenome}, {nome}. **{titulo}**: {subtitulo}. {cidade}: {editora}, {ano}."
                else:
                    ref = f"{sobrenome}, {nome}. **{titulo}**. {cidade}: {editora}, {ano}."
                
                st.success("✅ Copiada e formatada! Selecione e copie (Ctrl+C):")
                st.markdown(f"> {ref}")
            else:
                st.warning("Preencha todos os campos obrigatórios.")

    elif tipo == "Site / Artigo Online":
        st.subheader("🌐 Referência de Site")
        c1, c2 = st.columns(2)
        with c1:
            sobrenome_site = st.text_input("Sobrenome do Autor ou Nome do Site").upper()
            nome_site = st.text_input("Nome do Autor (se houver)")
        with c2:
            titulo_site = st.text_input("Título da Matéria/Artigo")
            ano_site = st.text_input("Ano de Publicação (ex: 2024)")
        
        link = st.text_input("Link de Acesso (URL)")
        data_acesso = st.text_input("Data de Acesso (ex: 25 fev. 2026)")

        if st.button("Gerar Referência ABNT"):
            if sobrenome_site and titulo_site and link and data_acesso:
                st.session_state.contador_ref += 1
                if nome_site:
                    ref_site = f"{sobrenome_site}, {nome_site}. {titulo_site}. **{sobrenome_site.title()}**, {ano_site}. Disponível em: <{link}>. Acesso em: {data_acesso}."
                else:
                    ref_site = f"**{sobrenome_site}**. {titulo_site}. {ano_site}. Disponível em: <{link}>. Acesso em: {data_acesso}."
                
                st.success("✅ Copiada e formatada! Selecione e copie (Ctrl+C):")
                st.markdown(f"> {ref_site}")
            else:
                st.warning("Preencha os campos principais.")

    # A MÁGICA NOVA DO DOI AQUI:
    elif tipo == "Artigo Científico (Automático via DOI) 🚀":
        st.subheader("🔬 Busca Automática")
        st.write("Digite o DOI do artigo e o sistema formatará a referência sozinho.")
        
        doi_input = st.text_input("Número do DOI (ex: 10.1038/s41586-020-2649-2)")

        if st.button("🔍 Buscar e Gerar ABNT"):
            if doi_input.strip():
                try:
                    # Limpa o input caso a pessoa tenha copiado o link inteiro
                    doi_limpo = doi_input.replace("https://doi.org/", "").strip()
                    
                    # Chama a API pública do Crossref
                    url = f"https://api.crossref.org/works/{doi_limpo}"
                    resposta = requests.get(url)

                    if resposta.status_code == 200:
                        dados = resposta.json()['message']
                        
                        # 1. Extraindo e formatando os Autores
                        autores_lista = []
                        for autor in dados.get('author', []):
                            sobrenome = autor.get('family', '').upper()
                            nome = autor.get('given', '')
                            if sobrenome:
                                autores_lista.append(f"{sobrenome}, {nome}")
                        autores_abnt = "; ".join(autores_lista) if autores_lista else "AUTOR DESCONHECIDO"

                        # 2. Extraindo Título, Revista e Ano
                        titulo_artigo = dados.get('title', ['Título não encontrado'])[0]
                        nome_revista = dados.get('container-title', ['Revista não informada'])[0]
                        
                        try:
                            ano_artigo = dados['issued']['date-parts'][0][0]
                        except:
                            ano_artigo = "s.d."
                            
                        volume = dados.get('volume', '')
                        numero = dados.get('issue', '')
                        paginas = dados.get('page', '')

                        # 3. Montando a String ABNT final
                        ref_doi = f"{autores_abnt}. {titulo_artigo}. **{nome_revista}**"
                        if volume:
                            ref_doi += f", v. {volume}"
                        if numero:
                            ref_doi += f", n. {numero}"
                        if paginas:
                            ref_doi += f", p. {paginas}"
                        ref_doi += f", {ano_artigo}. Disponível em: <https://doi.org/{doi_limpo}>."

                        # Incrementa o contador VIP e mostra a referência
                        st.session_state.contador_ref += 1
                        st.success("✅ Artigo encontrado e formatado!")
                        st.markdown(f"> {ref_doi}")
                        
                    else:
                        st.error("❌ DOI não encontrado. Verifique se digitou corretamente.")
                
                except Exception as e:
                    st.error("⚠️ Ocorreu um erro ao buscar o DOI. Tente novamente.")
            else:
                st.warning("Por favor, digite um DOI válido.")

# ==========================================
# LADO DIREITO: TEXTO DE APOIO E PIX
# ==========================================
with col_apoio:
    st.header("🎓 Apoie o Projeto")
    
    try:
        st.image("qrcode.png", caption="Escaneie para apoiar a Nico! ☕")
    except:
        st.info("Espaço para o QR Code (qrcode.png)")

    st.markdown("""
    ### 🛠️ Apoie uma Engenheira em Formação!
    
    Sou a **Nico**, 25 anos, futura Engenheira de Controle e Automação pelo **IFPA** (9º semestre). Desenvolvi este formatador para devolver o tempo que a burocracia da ABNT rouba de nós.
    
    **Por que o seu apoio é imprescindível hoje?** Na Engenharia, a inovação não acontece sentada em uma mesa. Ela acontece no laboratório, na bancada de robótica e no campo. Atualmente, meu desenvolvimento está "preso" a um PC fixo, o que é um gargalo crítico na minha reta final de curso.
    
    Ter um notebook funcional não é um luxo, é a **condição básica** para eu levar meus códigos para o laboratório e entregar meu TCC. 
    
    Ao apoiar, você não está apenas fazendo uma doação; você está **investindo no futuro da tecnologia nacional** e ajudando uma estudante a cruzar a linha de chegada.
    """)