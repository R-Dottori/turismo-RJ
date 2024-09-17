
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pag_1_title = 'Página 1 - Introdução'
pag_2_title = 'Página 2 - Carregando os Dados'
pag_3_title = 'Página 3 - Base de Dados'
pag_4_title = 'Página 4 - Visualizações'
pag_5_title = 'Página 5 - Métricas'
pag_6_title = 'Página 6 - Configurações da Página'


@st.cache_data
def subir_base(arquivo):
    df =  pd.read_csv(arquivo, index_col=0)
    return df
     

def cores():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {st.session_state['cor_fundo']};
        }}

        [data-testid=stSidebar] {{
            background-color: {st.session_state['cor_painel']} !important;
        }}

        h1, h2, h3, h4, h5, h6, p, div, span {{
            color: {st.session_state['cor_texto']} !important;
        }}
        """,
        unsafe_allow_html=True
    )


def pagina_inicial():
    if 'df' not in st.session_state:
        st.session_state['df'] = None

    if 'cor_fundo' not in st.session_state:
        st.session_state['cor_fundo'] = '#FFFFFF'

    if 'cor_painel' not in st.session_state:
        st.session_state['cor_painel'] = '#F0F2F6'

    if 'cor_texto' not in st.session_state:
        st.session_state['cor_texto'] = None

    cores()
    st.title('Turismo RJ')
    st.header(pag_1_title)

    st.markdown("""Esse é um painel interativo para explorar dados turísticos da cidade do Rio de Janeiro,
indicando o número de visitantes de diferentes países e continentes entre os anos de 2006 e 2019.

O aplicativo conta com diversas funcionalidades, como a de subir e salvar arquivos,
navegar em diferentes páginas para cada operação, explorar os dados de diferentes maneiras
(incluindo visualizações e métricas estatísticas), otimizar no carregamento dos dados, etc.""")

    st.image('https://jpimg.com.br/uploads/2023/05/turismo-no-rio-de-janeiro-veja-o-que-visitar-na-cidade-maravilhosa.jpg')

    st.markdown("""*Fonte dos dados:*
*Chegada mensal de turistas pelo Rio de Janeiro, por via Aérea, segundo continentes e países de residência permanente, entre 2006-2019*
*https://www.data.rio/documents/a6c6c3ff7d1947a99648494e0745046d/about*
""")


def pagina_dois():
    cores()
    st.header(pag_2_title)
    arquivo = st.file_uploader('Insira um arquivo CSV:', type='csv')
    if arquivo is not None:
        with st.spinner('Carregando...'):
            st.session_state['df'] = subir_base(arquivo)
            st.success('Base carregada com sucesso.')


def pagina_tres():
    cores()
    st.header(pag_3_title)
    if st.session_state['df'] is not None:
        st.write(st.session_state['df'])

        st.subheader('Filtros')
        filtro_periodo = st.radio('Selecione o formato:', options=['Todos os períodos', 'Por Mês'])

        if filtro_periodo == 'Todos os períodos':
            filtro_pais = st.selectbox('Selecione o país/continente que deseja exibir:', st.session_state['df'][st.session_state['df'].columns[0]].unique())
            df_filtrado = st.session_state['df'][st.session_state['df']['País/Continente'] == filtro_pais][['País/Continente', 'Total']]
            st.write(df_filtrado)
        
        else:
            filtro_mes = st.multiselect('Selecione quais períodos deseja exibir:', st.session_state['df'].columns[2:], default=st.session_state['df'].columns[2:])
            filtro_mes.insert(0, 'País/Continente')
            filtro_pais = st.selectbox('Selecione o país/continente que deseja exibir:', st.session_state['df'][st.session_state['df'].columns[0]].unique())
            df_filtrado = st.session_state['df'][st.session_state['df']['País/Continente'] == filtro_pais][filtro_mes]
            st.write(df_filtrado)

        st.subheader('Baixar dados filtrados')
        csv_filtrado = df_filtrado.to_csv()
        st.download_button(
            label='Baixar',
            data=csv_filtrado,
            file_name='csv_filtrado.csv'
        )
        
    else:
        st.warning('Aguardando o carregamento da base.')

    
def pagina_quatro():
    cores()
    st.header(pag_4_title)
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


def pagina_cinco():
    cores()
    st.header(pag_5_title)
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


def pagina_seis():
    st.header(pag_6_title)
    st.session_state['cor_fundo'] = st.color_picker('Selecione a cor do fundo:', value=st.session_state['cor_fundo'])
    st.session_state['cor_painel'] = st.color_picker('Selecione a cor da barra lateral:', value=st.session_state['cor_painel'])
    st.session_state['cor_texto'] = st.color_picker('Selecione a cor do texto:', value=st.session_state['cor_texto'])
    cores()



st.sidebar.title('Navegação')
pagina = st.sidebar.radio(label='Escolha uma página:', options=(pag_1_title, pag_2_title, pag_3_title, pag_4_title, pag_5_title, pag_6_title))
if pagina == pag_1_title:
    pagina_inicial()
elif pagina == pag_2_title:
    pagina_dois()
elif pagina == pag_3_title:
    pagina_tres()
elif pagina == pag_4_title:
    pagina_quatro()
elif pagina == pag_5_title:
    pagina_cinco()
else:
    pagina_seis()
