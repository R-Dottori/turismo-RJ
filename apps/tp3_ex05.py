
import streamlit as st
import pandas as pd
import time

st.title('Indicadores de Carregamento')

st.header('Subir a base de dados')
arquivo = st.file_uploader('Insira o arquivo CSV', type='csv')

if arquivo is not None:
    st.header('Base Original')
    with st.spinner('Carregando...'):
        df = pd.read_csv(arquivo, index_col=0)
        st.write(df)

    st.header('Filtros')
    
    filtro_mes = st.multiselect('Selecione quais períodos deseja exibir:', df.columns[2:], default=df.columns[2:])
    filtro_mes.insert(0, 'País/Continente')
    barra_progresso = st.progress(0, text='Aplicando filtros...')
    for percentual in range(100):
        time.sleep(0.001)
        barra_progresso.progress(percentual + 1, text='Aplicando filtros...')
    barra_progresso.empty()
    df_filtrado = df[filtro_mes]
    st.write(df_filtrado)
    
