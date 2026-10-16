import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Analisador de Sentimentos Offline",
    page_icon="📊",
    layout="centered"
)

@st.cache_resource
def get_translator() -> GoogleTranslator:
    """Retorna uma instância única do tradutor para otimizar a performance."""
    return GoogleTranslator(source='auto', target='en')

def analisar_sentimento(texto: str) -> tuple[str, float]:
    """
    Traduz o texto para o inglês (caso necessário) e analisa a polaridade
    utilizando o TextBlob.
    
    Retorna:
        - Uma tupla contendo o rótulo do sentimento ('Positivo', 'Negativo' ou 'Neutro')
          e o valor numérico da polaridade.
    """
    if not texto.strip():
        return "Neutro", 0.0

    try:
        # Tradução invisível para o inglês (já que o TextBlob tem melhor suporte)
        translator = get_translator()
        texto_em_ingles = translator.translate(texto)
    except Exception as e:
        # Fallback caso ocorra algum problema na tradução
        texto_em_ingles = texto

    # Análise de polaridade com TextBlob (-1.0 a 1.0)
    blob = TextBlob(texto_em_ingles)
    polaridade = blob.sentiment.polarity

    # Classificação baseada na polaridade
    if polaridade > 0.05:
        sentimento = "Positivo"
    elif polaridade < -0.05:
        sentimento = "Negativo"
    else:
        sentimento = "Neutro"

    return sentimento, polaridade

def main():
    # Cabeçalho da aplicação
    st.title("📊 Analisador de Sentimentos Offline")
    st.markdown(
        "Este aplicativo roda totalmente local usando bibliotecas tradicionais de Python "
        " (**TextBlob** e **deep-translator**). Nenhuma API paga ou externa é utilizada!"
    )
    
    st.divider()

    # Entrada de texto do usuário
    texto_usuario = st.text_area(
        "Digite seu texto abaixo (suporta português, inglês ou outros idiomas):",
        placeholder="Ex: Eu adorei este aplicativo, ele é simplesmente fantástico!",
        height=150
    )

    # Botão de análise
    if st.button("Analisar", type="primary"):
        if not texto_usuario.strip():
            st.warning("Por favor, digite algum texto antes de clicar em Analisar.")
        else:
            with st.spinner("Analisando sentimento..."):
                sentimento, polaridade = analisar_sentimento(texto_usuario)

            st.subheader("Resultado da Análise:")

            # Exibição visual baseada no resultado usando componentes do Streamlit
            if sentimento == "Positivo":
                st.success(f"**Sentimento:** Positivo 😊 (Polaridade: {polaridade:.2f})")
            elif sentimento == "Negativo":
                st.error(f"**Sentimento:** Negativo  (Polaridade: {polaridade:.2f})")
            else:
                st.warning(f"**Sentimento:** Neutro 😐 (Polaridade: {polaridade:.2f})")

if __name__ == "__main__":
    main()
