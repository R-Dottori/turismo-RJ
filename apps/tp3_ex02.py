
import streamlit as st
import pandas as pd

st.title('Subir um arquivo em CSV')

df = st.file_uploader('Insira o arquivo CSV', type='csv')

if df is not None:
    df = pd.read_csv(df, index_col=0)
    st.write(df)
