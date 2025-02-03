import streamlit as st
import requests

# Injeção de CSS customizado para permitir redimensionamento vertical
# e garantir que o texto faça a quebra automática de linha.
st.markdown(
    """
    <style>
    /* Aplica o estilo somente à textarea com o aria-label específico */
    textarea[aria-label="Enter your Text:"] {
        resize: vertical;         /* Permite redimensionar verticalmente */
        overflow-wrap: break-word; /* Garante quebra de linha automática */
        white-space: pre-wrap;     /* Preserva quebras de linha */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Exibe a logo no header de forma responsiva utilizando o parâmetro atualizado
st.image("https://www.tutorialmaster.org/gpt/dante_header_V2.jpg", use_container_width=True)

# Título do aplicativo atualizado para "Assistente virtual para Registro de Imoveis | SC." com tamanho H3
st.markdown("### Assistente virtual para Registro de Imoveis")

# Define a URL da API
api_url = "https://brazilian-laws-chatbot.onrender.com/query-llm"
# Para testes locais, você pode usar:
# api_url = "http://127.0.0.1:5000/query-llm"

# Caixa de entrada para o prompt utilizando st.text_area com altura configurada (aproximadamente 5 linhas)
prompt = st.text_area("Enter your Text:", height=120)

# Função para chamar a API REST e retornar a resposta
def get_response_from_api(prompt):
    try:
        # Define o payload
        payload = {"query": prompt}
        # Faz uma requisição POST para a API
        response = requests.post(api_url, json=payload)
        # Verifica se a resposta foi bem sucedida
        if response.status_code == 200:
            return response.json().get("gpt_response", "No response from API.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Botão para gerar a resposta
if st.button("Generate Response"):
    with st.spinner('Generating response...'):
        # Busca a resposta na API
        response = get_response_from_api(prompt)
        # Exibe a resposta na interface
        st.write(response)
