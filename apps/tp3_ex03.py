
import streamlit as st
import pandas as pd

st.title('Filtro de Dados e Seleção')

st.header('Subir a base de dados')
df = st.file_uploader('Insira o arquivo CSV', type='csv')

if df is not None:
    st.header('Base Original')
    df = pd.read_csv(df, index_col=0)
    st.write(df)

    st.header('Filtros')
    filtro_periodo = st.radio('Selecione o formato:', options=['Todos os períodos', 'Por Mês'])

    if filtro_periodo == 'Todos os períodos':
        filtro_pais = st.selectbox('Selecione o país/continente que deseja exibir:', df[df.columns[0]].unique())
        df_filtrado = df[df['País/Continente'] == filtro_pais][['País/Continente', 'Total']]
        st.write(df_filtrado)
    
    else:
        filtro_mes = st.multiselect('Selecione quais períodos deseja exibir:', df.columns[2:], default=df.columns[2:])
        filtro_mes.insert(0, 'País/Continente')
        filtro_pais = st.selectbox('Selecione o país/continente que deseja exibir:', df[df.columns[0]].unique())
        df_filtrado = df[df['País/Continente'] == filtro_pais][filtro_mes]
        st.write(df_filtrado)
