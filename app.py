import streamlit as st
from PIL import Image
import pandas as pd

@st.cache_data
def load_df(arquivo):
    return pd.read_csv(arquivo)

def image_to_base64(image):
    from io import BytesIO
    import base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def load_mobile(perfis_df):
    for _, row in perfis_df.iterrows():
        with st.container():
            st.markdown('<div class="mobile-profile mobile-spacing">', unsafe_allow_html=True)
            arquivo = './perfis/' + row["instagram"]+'.jpg'
            try:
                imagem = Image.open(arquivo)
                st.markdown(
                    f"""
                    <a href='{row['url']}' target='_blank'>
                        <img src='data:image/png;base64,{image_to_base64(imagem)}' 
                                alt='{row["nome"]}' 
                                class='clickable-image mobile-image'>
                    </a>
                    <p class='company-name'>{row["nome"]}</p>
                    """,
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Erro ao carregar {arquivo}")
            st.markdown('</div>', unsafe_allow_html=True)

def load_desktop(perfis_df):
    cols = st.columns(4)
    for idx, (_, row) in enumerate(perfis_df.iterrows()):
        arquivo = './perfis/' + row["instagram"]+'.jpg'
        with cols[idx % 4]:
            try:
                imagem = Image.open(arquivo)
                st.markdown(
                    f"""
                    <div class="desktop-profile">
                        <a href='{row['url']}' target='_blank'>
                            <img src='data:image/png;base64,{image_to_base64(imagem)}' 
                                    alt='{row["nome"]}' 
                                    class='clickable-image desktop-image'>
                        </a>
                        <p class='company-name'>{row["nome"]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Erro ao carregar {arquivo}")    

# Configuração da página
st.set_page_config(page_title="Encontro ALI Produtividade", layout="wide", page_icon="📸")

# Aplicar CSS personalizado
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
    
    .search-container {
        margin-bottom: 1rem !important;
    }
    
    /* Layout para mobile */
    @media (max-width: 768px) {
        .desktop-view {
            display: none !important;
        }
        
        .mobile-view {
            display: block !important;
        }
        
        .main .block-container {
            padding: 0.5rem 0.5rem 0.25rem;
        }
        
        h1 {
            font-size: 1.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        h3 {
            font-size: 1.2rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .stTextInput>div>div>input {
            width: 100% !important;
            margin-bottom: 0.5rem !important;
        }
        
        .mobile-profile {
            width: 100% !important;
            max-width: 180px !important;
            margin: 0.5rem auto !important;
            padding: 0 !important;
        }
        
        .mobile-image {
            max-width: 150px !important;
            height: auto !important;
        }
        
        .mobile-spacing {
            margin-bottom: 1rem !important;
        }
    }
    
    /* Layout para desktop */
    @media (min-width: 769px) {
        .mobile-view {
            display: none !important;
        }
        
        .desktop-view {
            display: block !important;
        }
        
        .desktop-columns {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .desktop-profile {
            text-align: center;
        }
        
        .desktop-image {
            max-width: 120px !important;
            height: auto !important;
        }
    }
    
    .clickable-image {
        transition: transform 0.2s;
        cursor: pointer;
        border: 2px solid var(--border-color);
        width: 100%;
        aspect-ratio: 1/1;
        object-fit: cover;
        border-radius: 8px;
        margin: 0 auto;
        display: block;
    }
    
    .clickable-image:hover {
        transform: scale(1.03);
        opacity: 0.9;
        border-color: var(--link-color);
    }
    
    .company-name {
        color: var(--text-color);
        font-weight: 500;
        margin-top: 0.5rem;
        font-size: 0.9rem;
        text-align: center;
        word-break: break-word;
    }
    
    .author-credit {
        text-align: center;
        margin-top: 1rem;
        font-size: 0.75rem;
        color: #777777;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título do aplicativo
st.title("Encontro ALI Produtividade")
st.markdown("<h3>Perfis de Empresas no Instagram</h3>", unsafe_allow_html=True)

# Carregar dados
try:
    perfis_df = load_df("dados_perfis.csv")
except:
    st.error("Verifique se 'dados_perfis.csv'.")

# Verificar o tamanho da tela e mostrar apenas uma visualização
if st.session_state.get('is_mobile', False):
    # Layout para mobile
    load_mobile(perfis_df)
else:
    # Layout para desktop
    load_desktop(perfis_df)

# Créditos
st.markdown(
    """
    <div class='author-credit'>
        Desenvolvido por <a href='https://www.instagram.com/mmmarcelom' target='_blank'>Marcelo Mesquita</a>
    </div>
    """,
    unsafe_allow_html=True
)