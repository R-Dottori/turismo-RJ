
import streamlit as st
import pandas as pd

st.title('Alterar Cores')

st.header('Opções de Cor')
cor_fundo = st.color_picker('Selecione a cor do fundo:', value='#FFFFFF')
cor_texto = st.color_picker('Selecione a cor do texto:')
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {cor_fundo};
    }}

    h1, h2, h3, h4, h5, h6, p, div, span {{
        color: {cor_texto} !important;
    }}
    """,
    unsafe_allow_html=True
)

st.header('Subir a base de dados')
arquivo = st.file_uploader('Insira o arquivo CSV', type='csv')

if arquivo is not None:
    st.header('Base Original')
    df = pd.read_csv(arquivo, index_col=0)
    st.write(df)
