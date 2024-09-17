
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pag_1_title = 'Página 1 - Carregando os Dados'
pag_2_title = 'Página 2 - Base de Dados'
pag_3_title = 'Página 3 - Visualizações'


@st.cache_data
def subir_base(arquivo):
    df =  pd.read_csv(arquivo, index_col=0)
    return df
     

def pagina_inicial():
    st.title('Visualizações')
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
        st.subheader('Distribuição de Turistas por Mês')
        filtro_mes = st.multiselect('Selecione os meses:', st.session_state['df'].columns[2:], default=st.session_state['df'].columns[2:])
        df_mes = st.session_state['df'][filtro_mes]
        fig_mes, ax_mes = plt.subplots()
        ax_mes = sns.barplot(df_mes)
        plt.xticks(rotation=90)
        st.write(fig_mes)

        st.subheader('Distribuição de Turistas por Continente')
        continentes = ['África', 'América Central', 'América do Norte', 'América do Sul',
                       'Ásia', 'Europa', 'Oceania', 'Oriente Médio', 'Países não especificados']
        filtro_cont = st.multiselect('Selecione os continentes:', continentes, default=continentes)
        df_cont = st.session_state['df'][st.session_state['df']['País/Continente'].isin(filtro_cont)]
        fig_cont, ax_cont = plt.subplots()
        ax_cont = sns.barplot(data=df_cont, x='País/Continente', y='Total')
        plt.xticks(rotation=90)
        plt.ylabel('')
        plt.xlabel('')
        st.write(fig_cont)
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
