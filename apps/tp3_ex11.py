
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pag_1_title = 'Página 1 - Carregando os Dados'
pag_2_title = 'Página 2 - Base de Dados'
pag_3_title = 'Página 3 - Scatter Plot'


@st.cache_data
def subir_base(arquivo):
    df =  pd.read_csv(arquivo, index_col=0)
    return df
     

def pagina_inicial():
    st.title('Visualização Avançada')
    st.header(pag_1_title)

    if 'df' not in st.session_state:
        st.session_state['df'] = None

    arquivo = st.file_uploader('Insira um arquivo CSV:', type='csv')
    if arquivo is not None:
        st.session_state['df'] = subir_base(arquivo)
        st.success('Base carregada com sucesso.')


def pagina_dois():
    st.header(pag_2_title)
    if st.session_state['df'] is not None:
        st.write(st.session_state['df'])
    else:
        st.warning('Aguardando o carregamento da base.')


def pagina_tres():
    st.header(pag_3_title)
    if st.session_state['df'] is not None:
        filtro_mes = st.radio('Selecione o período:', st.session_state['df'].columns[1:])
        continentes = ['África', 'América Central', 'América do Norte', 'América do Sul',
                       'Ásia', 'Europa', 'Oceania', 'Oriente Médio', 'Países não especificados']
        filtro_cont = st.multiselect('Selecione os continentes:', continentes, default=continentes)
        fig, ax = plt.subplots()
        ax = sns.scatterplot(st.session_state['df'][st.session_state['df']['País/Continente'].isin(filtro_cont)], x='País/Continente', y=filtro_mes)
        plt.ylabel(f'Turistas - {filtro_mes}')
        plt.xlabel('')
        plt.xticks(rotation=90)
        plt.grid(axis='y')
        st.write(fig)
    else:
        st.warning('Aguardando o carregamento da base.')


st.sidebar.title('Navegação')
pagina = st.sidebar.radio(label='Escolha uma página:', options=(pag_1_title, pag_2_title, pag_3_title))
if pagina == pag_1_title:
    pagina_inicial()
elif pagina == pag_2_title:
    pagina_dois()
else:
    pagina_tres()
