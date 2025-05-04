import streamlit as st
from PIL import Image
import pandas as pd
import os

# Configuração da página com meta tag para mobile
st.set_page_config(
    page_title="Encontro ALI Produtividade",
    layout="wide",
    page_icon="📸"
)

# Aplicar CSS personalizado com media queries para mobile
st.markdown(
    """
    <style>
    :root {
        --primary-color: #f63366;
        --background-color: #f5f5f5;
        --secondary-background-color: #e8e8e8;
        --text-color: #333333;
        --border-color: #d0d0d0;
        --link-color: #1e88e5;
    }
    
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    /* Espaço maior abaixo da barra de pesquisa */
    .search-spacer {
        margin-bottom: 2rem !important;
        padding-bottom: 1.5rem !important;
    }
    
    /* Ajustes gerais para mobile */
    @media (max-width: 768px) {
        /* Reduz padding e margens */
        .main .block-container {
            padding: 1rem 1rem 0.5rem;
        }
        
        /* Ajusta tamanho dos títulos */
        h1 {
            font-size: 1.5rem !important;
        }
        
        h3 {
            font-size: 1.2rem !important;
        }
        
        /* Barra de pesquisa ocupando toda largura */
        .stTextInput>div>div>input {
            width: 100% !important;
        }
        
        /* Espaço menor em mobile */
        .search-spacer {
            margin-bottom: 1.5rem !important;
            padding-bottom: 1rem !important;
        }
    }
    
    .stTextInput>div>div>input {
        background-color: white;
        color: var(--text-color);
        border: 1px solid var(--border-color);
    }
    
    .css-1aumxhk {
        background-color: var(--secondary-background-color);
    }
    
    .st-b7, .st-c0 {
        color: var(--text-color);
    }
    
    .stMarkdown a {
        color: var(--link-color) !important;
    }
    
    .stWarning, .stError {
        color: #000000;
    }
    
    /* Imagens responsivas */
    .clickable-image {
        transition: transform 0.2s;
        cursor: pointer;
        border: 2px solid var(--border-color);
        max-width: 100%;
        height: auto;
    }
    
    .clickable-image:hover {
        transform: scale(1.03);
        opacity: 0.9;
        border-color: var(--link-color);
    }
    
    .company-name {
        color: var(--text-color);
        font-weight: 500;
        margin-top: 8px;
        font-size: 0.9rem;
        word-break: break-word;
    }
    
    /* Rodapé mobile */
    .author-credit {
        text-align: center;
        margin-top: 20px;
        font-size: 0.75rem;
        color: #777777;
        padding-bottom: 10px;
    }
    
    .author-credit a {
        color: #777777 !important;
        text-decoration: none;
    }
    
    .author-credit a:hover {
        color: #555555 !important;
        text-decoration: underline;
    }
    
    /* Grid responsivo - 2 colunas em mobile */
    @media (max-width: 768px) {
        .responsive-column {
            width: 48% !important;
            margin: 1% !important;
            float: left !important;
            box-sizing: border-box !important;
        }
        
        /* Limpar floats */
        .row::after {
            content: "";
            display: table;
            clear: both;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título do aplicativo
st.title("Encontro ALI Produtividade")
st.markdown("<h3 style='color: var(--text-color);'>Perfis de Empresas no Instagram</h3>", unsafe_allow_html=True)

# Carregar dados do CSV
@st.cache_data
def carregar_dados():
    return pd.read_csv("dados_perfis.csv")

# Função para converter imagem para base64
def image_to_base64(image):
    from io import BytesIO
    import base64
    
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

try:
    perfis_df = carregar_dados()
    # Adicionar barra de pesquisa com container para espaçamento
    with st.container():
        termo_pesquisa = st.text_input("Pesquisar empresa...")
        # Div para criar espaço abaixo da barra de pesquisa
        st.markdown('<div class="search-spacer"></div>', unsafe_allow_html=True)
    
    if termo_pesquisa:
        perfis_df = perfis_df[perfis_df['nome'].str.contains(termo_pesquisa, case=False)]
    
    # Layout responsivo - 4 colunas em desktop, 2 em mobile
    colunas_por_linha = 4
    
    # Usar container para melhor controle em mobile
    container = st.container()
    
    # Exibir cada perfil
    for i, row in perfis_df.iterrows():
        # Nova linha a cada 4 itens (desktop) ou 2 itens (mobile via CSS)
        if i % colunas_por_linha == 0:
            cols = container.columns(colunas_por_linha)
        
        with cols[i % colunas_por_linha]:
            try:
                imagem = Image.open('./perfis/' + row["imagem"])
                
                st.markdown(
                    f"""
                    <div class="responsive-column">
                        <div style='text-align: center; margin-bottom: 15px;'>
                            <a href='{row['link']}' target='_blank'>
                                <img src='data:image/png;base64,{image_to_base64(imagem)}' 
                                     alt='{row["nome"]}' 
                                     style='width: 100%; max-width: 150px; height: auto; aspect-ratio: 1/1; object-fit: cover; border-radius: 8px;'
                                     class='clickable-image'>
                            </a>
                            <p class='company-name'>{row["nome"]}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            except FileNotFoundError:
                st.warning(f"Imagem não encontrada para {row['nome']}, {row['imagem']}")
            except Exception as e:
                st.error(f"Erro ao carregar {row['nome']}: {str(e)}")

except FileNotFoundError:
    st.error("Arquivo de perfis não encontrado. Por favor, verifique se 'dados_perfis.csv' existe.")

# Créditos do autor (discreto no final)
st.markdown(
    """
    <div class='author-credit'>
        Desenvolvido por <a href='https://www.instagram.com/mmmarcelom' target='_blank'>Marcelo Mesquita</a>
    </div>
    """,
    unsafe_allow_html=True
)