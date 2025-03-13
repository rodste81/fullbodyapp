import streamlit as st
import sqlite3
import pandas as pd
from db import get_connection  # Importa a conexão do banco de dados

# Função para listar todas as tabelas do banco
def listar_tabelas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    conn.close()
    return [t[0] for t in tabelas]

# Função para visualizar os dados de uma tabela específica
def visualizar_tabela(nome_tabela):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {nome_tabela}", conn)
    conn.close()
    return df

# Função para carregar a interface administrativa
def carregar_admin():
    st.title("🔧 Painel Administrativo")

    tabelas = listar_tabelas()
    tabela_selecionada = st.selectbox("Escolha uma tabela para visualizar:", tabelas)

    if tabela_selecionada:
        df_tabela = visualizar_tabela(tabela_selecionada)
        st.write(f"📋 Exibindo dados da tabela **{tabela_selecionada}**")
        st.dataframe(df_tabela)
