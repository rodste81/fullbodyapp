import streamlit as st
from auth import login
from menus import carregar_conteudo_menu
from db import criar_banco, get_connection
from admin import carregar_admin  # Importa o painel de administração
import os

# Criar banco de dados apenas se não existir
if not os.path.exists("workout2.db"):
    criar_banco()
    print("✅ Banco de dados criado e pronto para uso!")

# Verifica se o usuário está logado
if "usuario" not in st.session_state or "usuario_id" not in st.session_state:
    login()
    st.stop()

# Obtém o ID e nome do usuário logado
usuario_id = st.session_state.get("usuario_id")
usuario_nome = st.session_state.get("usuario")

# Configurar Sidebar
st.sidebar.title(f"👤 Usuário: {usuario_nome}")

# Definição do menu com "Admin" apenas para o usuário "rod"
opcoes_menu = ["Peitorais", "Costas", "Ombro", "Biceps", "Triceps", "Pernas", "Abdomen", "Cadastrar Exercício", "Make iT!", "Histórico de Treinos", "Sair"]

if usuario_nome == "rod":
    opcoes_menu.insert(0, "Admin")  # Adiciona "Admin" no topo do menu

menu = st.sidebar.radio("Menu", opcoes_menu)

# Executa o menu selecionado
if menu == "Admin":
    carregar_admin()
elif menu == "Sair":
    st.session_state.clear()
    st.rerun()
else:
    carregar_conteudo_menu(menu, usuario_id)
