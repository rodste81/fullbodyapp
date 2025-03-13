import streamlit as st
from auth import login
from menus import carregar_conteudo_menu
from db import criar_banco, get_connection
from admin import carregar_admin  # Importa o painel de administração

criar_banco()  # Garante que o banco seja criado antes de rodar o app


# Verifica se o usuário está logado
if "usuario" not in st.session_state or "usuario_id" not in st.session_state:
    login()
    st.stop()

usuario_id = st.session_state["usuario_id"]

# Se o usuário for "rod", incluir o menu "Admin"
if st.session_state["usuario"] == "rod":
    menu = st.sidebar.radio("Menu", ["Admin", "Peitorais", "Costas", "Ombro", "Biceps", "Triceps", "Pernas", "Abdomen", "Cadastrar Exercício", "Make iT!", "Histórico de Treinos", "Sair"])
else:
    menu = st.sidebar.radio("Menu", ["Peitorais", "Costas", "Ombro", "Biceps", "Triceps", "Pernas", "Abdomen", "Cadastrar Exercício", "Make iT!", "Histórico de Treinos", "Sair"])

# Chamar função correspondente ao menu escolhido
if menu == "Admin" and st.session_state["usuario"] == "rod":
    carregar_admin()
    
# Garantindo que os menus apareçam corretamente
st.sidebar.title(f"👤 Usuário: {st.session_state['usuario']}")
menu = st.sidebar.radio("Menu", ["Peitorais", "Costas", "Ombro", "Biceps", "Triceps", "Pernas", "Abdomen", "Cadastrar Exercício", "Make iT!", "Histórico de Treinos", "Sair"])

# Carregar o conteúdo do menu selecionado com o usuario_id correto
if menu == "Sair":
    st.session_state.clear()
    st.rerun()
else:
    carregar_conteudo_menu(menu, usuario_id)
