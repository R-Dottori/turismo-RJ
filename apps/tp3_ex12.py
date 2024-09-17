
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pag_1_title = 'Página 1 - Carregando os Dados'
pag_2_title = 'Página 2 - Base de Dados'
pag_3_title = 'Página 3 - Métricas'


@st.cache_data
def subir_base(arquivo):
    df =  pd.read_csv(arquivo, index_col=0)
    return df
     

def pagina_inicial():
    st.title('Métricas Básicas')
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
        continentes = ['África', 'América Central', 'América do Norte', 'América do Sul',
                       'Ásia', 'Europa', 'Oceania', 'Oriente Médio', 'Países não especificados']
        excl = [continente for continente in continentes]
        excl.append('   Outros')
        excl.append('Total')
        st.session_state['df']['Média Mensal'] = st.session_state['df'].drop(st.session_state['df'].columns[:2], axis=1).mean(axis=1)
        paises = st.session_state['df'][~st.session_state['df']['País/Continente'].isin(excl)]
        st.subheader('Média de visitantes mensais por Continente')
        st.write(f'{len(continentes)} continentes')
        st.write(st.session_state['df'][st.session_state['df']['País/Continente'].isin(continentes)][['País/Continente', 'Média Mensal']])
        st.subheader(f'Média de visitantes mensais por Países Especificados')
        st.write(f'{paises.shape[0]} países especificados')
        st.write(paises[['País/Continente', 'Média Mensal']])
        st.subheader('Total de Visitas em cada Estação por Países Especificados')
        paises['Verão (Jan-Mar)'] = paises[['Janeiro', 'Fevereiro', 'Março']].sum(axis=1)
        paises['Outono (Abr-Jun)'] = paises[['Abril', 'Maio', 'Junho']].sum(axis=1)
        paises['Inverno (Jul-Set)'] = paises[['Julho', 'Agosto', 'Setembro']].sum(axis=1)
        paises['Primavera (Out-Dez)'] = paises[['Outubro', 'Novembro', 'Dezembro']].sum(axis=1)
        st.write(paises[['País/Continente', 'Verão (Jan-Mar)', 'Outono (Abr-Jun)', 'Inverno (Jul-Set)', 'Primavera (Out-Dez)']])
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
