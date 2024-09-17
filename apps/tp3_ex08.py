
import streamlit as st
import pandas as pd
import time

pag_1_title = 'Página 1 - Carregando os Dados'
pag_2_title = 'Página 2 - Exibindo a Base de Dados'
pag_3_title = 'Página 3 - Filtrando os Dados'


@st.cache_data
def subir_base(arquivo):
    df = pd.read_csv(arquivo, index_col=0)
    return df


def pagina_inicial():
    st.title('Persistência de Dados')
    st.header(pag_1_title)
    
    if 'df' not in st.session_state:
        st.session_state['df'] = None
    
    if 'filtro' not in st.session_state:
        st.session_state['filtro'] = []

    arquivo = st.file_uploader('Insira um arquivo CSV:', type='csv')
    if arquivo is not None:
        st.session_state['df'] = subir_base(arquivo)
        st.session_state['filtro'] = []


def pagina_dois():
    st.header(pag_2_title)
    if st.session_state['df'] is not None:
        st.write(st.session_state['df'])
    else:
        st.write('Aguardando o carregamento da base.')


def pagina_tres():
    st.header(pag_3_title)
    if st.session_state['df'] is not None:
        st.session_state['filtro'] = st.multiselect('Selecione as colunas:', st.session_state['df'].columns, default=st.session_state['filtro'])
        
        df_filtrado = st.session_state['df'][st.session_state['filtro']]
        st.write(df_filtrado)
    else:
        st.write('Aguardando o carregamento da base.')


st.sidebar.title('Navegação')
pagina = st.sidebar.radio(label='Escolha uma página:', options=(pag_1_title, pag_2_title, pag_3_title))
if pagina == pag_1_title:
    pagina_inicial()
elif pagina == pag_2_title:
    pagina_dois()
else:
    pagina_tres()
