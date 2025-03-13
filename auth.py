import streamlit as st
import bcrypt
from db import get_connection, obter_usuario_id

def verificar_login(username, senha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT senha_hash FROM usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(senha.encode('utf-8'), user[0]):
        return True
    return False

def cadastrar_usuario(username, senha):
    conn = get_connection()
    cursor = conn.cursor()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO usuarios (username, senha_hash) VALUES (?, ?)", (username, senha_hash))
        conn.commit()
        st.success(f"✅ Usuário {username} cadastrado com sucesso! Agora você pode fazer login.")
    except sqlite3.IntegrityError:
        st.error(f"⚠️ O usuário {username} já existe. Escolha outro nome.")

    conn.close()

def login():
    st.title("🔐 Login")

    tab1, tab2 = st.tabs(["Entrar", "Cadastrar"])

    with tab1:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Usuário", key="login_user")
            senha = st.text_input("Senha", type="password", key="login_pass")
            submitted = st.form_submit_button("Entrar")

            if submitted:
                if verificar_login(username, senha):
                    st.session_state["usuario"] = username
                    st.session_state["usuario_id"] = obter_usuario_id(username)
                    st.success(f"✅ Bem-vindo, {username}!")
                    st.rerun()
                else:
                    st.error("⚠️ Usuário ou senha incorretos")

    with tab2:
        with st.form("register_form", clear_on_submit=False):
            new_username = st.text_input("Novo Usuário", key="register_user")
            new_senha = st.text_input("Nova Senha", type="password", key="register_pass")
            confirm_senha = st.text_input("Confirme a Senha", type="password", key="register_confirm")
            submitted_register = st.form_submit_button("Cadastrar")

            if submitted_register:
                if new_senha != confirm_senha:
                    st.error("⚠️ As senhas não coincidem.")
                elif new_username and new_senha:
                    cadastrar_usuario(new_username, new_senha)
                else:
                    st.error("⚠️ Preencha todos os campos.")
