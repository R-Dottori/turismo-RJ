
import streamlit as st
import pandas as pd


@st.cache_data
def subir_base(arquivo):
    df = pd.read_csv(arquivo, index_col=0)
    return df


st.title('Tabela Interativa')

arquivo = st.file_uploader('Insira um arquivo CSV:', type='csv')

if arquivo is not None:
    st.header('Base de Dados')
    st.write('Podemos usar o mesmo elemento que utilizamos nos outros aplicativos, que já conta com funcionalidades de busca e ordenação.')
    df = subir_base(arquivo)
    st.dataframe(df)
