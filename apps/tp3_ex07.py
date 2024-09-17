
import streamlit as st
import pandas as pd
import time


@st.cache_data
def subir_base(arquivo):
    df = pd.read_csv(arquivo, index_col=0)
    return df


st.title('Teste de Cache')

arquivo = st.file_uploader('Insira um arquivo CSV:', type='csv')

if arquivo is not None:
    st.header('Base Original')
    with st.spinner('Carregando...'):
        inicio = time.time()
        df = subir_base(arquivo)
        st.write(df)
        st.write(f'Tempo de Carregamento: {time.time() - inicio}')
