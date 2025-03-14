import streamlit as st
import sqlite3
import random
import datetime
import pandas as pd
from db import get_connection

def listar_exercicios(grupo, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM exercicios WHERE grupo = ? AND usuario_id = ?", (grupo, usuario_id))
    exercicios = cursor.fetchall()
    conn.close()
    return exercicios

def adicionar_exercicio(nome, grupo, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    # 🔍 Verifica se o exercício já existe para o usuário
    cursor.execute("SELECT id FROM exercicios WHERE nome = ? AND grupo = ? AND usuario_id = ?", (nome, grupo, usuario_id))
    existe = cursor.fetchone()

    if existe:
        st.warning("⚠️ Este exercício já está cadastrado!")
        conn.close()
        return  # ⛔️ Para a execução aqui, evitando o INSERT

    # Se não existir, faz o cadastro e exibe a mensagem de sucesso
    cursor.execute("INSERT INTO exercicios (nome, grupo, usuario_id) VALUES (?, ?, ?)", (nome, grupo, usuario_id))
    conn.commit()
    
    #st.success("✅ Exercício cadastrado com sucesso!")  # ✅ Agora só aparece se realmente for inserido

    conn.close()




def remover_exercicio(exercicio_id, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exercicios WHERE id = ? AND usuario_id = ?", (exercicio_id, usuario_id))
    conn.commit()
    conn.close()

def gerar_treino(quantidades, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    grupos = ["Peitorais", "Costas", "Ombro", "Biceps", "Triceps", "Pernas", "Abdomen"]
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    treino = {dia: {grupo: [] for grupo in grupos} for dia in dias_semana}
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for grupo in grupos:
        cursor.execute("SELECT nome FROM exercicios WHERE grupo = ? AND usuario_id = ?", (grupo, usuario_id))
        exercicios = [row[0] for row in cursor.fetchall()]
        random.shuffle(exercicios)

        if not exercicios:
            continue

        if len(exercicios) < quantidades.get(grupo, 1) * len(dias_semana):
            multiplicador = (quantidades.get(grupo, 1) * len(dias_semana)) // max(len(exercicios), 1) + 1
            exercicios *= multiplicador

        index = 0
        for dia in dias_semana:
            treino[dia][grupo] = exercicios[index:index + quantidades.get(grupo, 1)]
            index += quantidades.get(grupo, 1)

            for exercicio in treino[dia][grupo]:
                cursor.execute("INSERT INTO treinos (data, dia, grupo, exercicio, usuario_id) VALUES (?, ?, ?, ?, ?)",
                               (data_atual, dia, grupo, exercicio, usuario_id))

    conn.commit()
    conn.close()
    return treino, dias_semana

def listar_treinos(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT data FROM treinos WHERE usuario_id = ? ORDER BY data DESC", (usuario_id,))
    datas = [row[0] for row in cursor.fetchall()]

    treinos_agrupados = {}
    for data in datas:
        cursor.execute("SELECT dia, grupo, exercicio FROM treinos WHERE data = ? AND usuario_id = ? ORDER BY dia", (data, usuario_id))
        treinos = cursor.fetchall()

        treino_tabela = {"Dia": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]}
        for grupo in ["Peitorais", "Costas", "Ombro", "Biceps", "Triceps", "Pernas", "Abdomen"]:
            treino_tabela[grupo] = []

        for dia in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]:
            grupo_dict = {grupo: [] for grupo in ["Peitorais", "Costas", "Ombro", "Biceps", "Triceps", "Pernas", "Abdomen"]}
            for t in treinos:
                if t[0] == dia:
                    grupo_dict[t[1]].append(t[2])

            for grupo in grupo_dict.keys():
                treino_tabela[grupo].append(", ".join(grupo_dict[grupo]))

        treinos_agrupados[data] = pd.DataFrame(treino_tabela)

    conn.close()
    return treinos_agrupados

def deletar_treino(data_treino, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM treinos WHERE data = ? AND usuario_id = ?", (data_treino, usuario_id))
    conn.commit()
    conn.close()

def carregar_conteudo_menu(menu, usuario_id):
    if menu in ["Peitorais", "Costas", "Ombro", "Biceps", "Triceps", "Pernas", "Abdomen"]:
        st.title(f"🏋️ Exercícios para {menu}")
        exercicios = listar_exercicios(menu, usuario_id)
        if not exercicios:
            st.write("⚠️ Nenhum exercício cadastrado para este grupo.")
        else:
            for ex in exercicios:
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    st.write(f"{ex[1]}")
                with col2:
                    if st.button("🗑", key=f"del_{ex[0]}"):
                        remover_exercicio(ex[0], usuario_id)
                        st.success(f"Exercício {ex[1]} removido com sucesso!")
                        st.rerun()

    elif menu == "Cadastrar Exercício":
        st.title("➕ Cadastrar Novo Exercício")
        nome = st.text_input("Nome do Exercício")
        grupo = st.selectbox("Grupo Muscular", ["Peitorais", "Costas", "Ombro", "Biceps", "Triceps", "Pernas", "Abdomen"])
        if st.button("Salvar"):
            adicionar_exercicio(nome, grupo, usuario_id)
            st.success("✅ Exercício cadastrado com sucesso!")

    elif menu == "Make iT!":
        st.title("🔥 Gerar Treino Semanal Full Body")
        st.write("Defina a ênfase para cada grupo muscular")

        # 🆕 Alteração: Agora a ênfase pode ser escolhida com `st.radio`**
        grupos = ["Peitorais", "Costas", "Ombro", "Biceps", "Triceps", "Pernas", "Abdomen"]
        quantidades = {grupo: 1 for grupo in grupos}  # Valor padrão

        for grupo in grupos:
            quantidades[grupo] = int(st.radio(f"📌 {grupo} - Quantidade de exercícios por dia", [1, 2, 3], index=0))

        if st.button("🚀 Gerar Treino"):
            treino, dias_semana = gerar_treino(quantidades, usuario_id)
            st.success("✅ Treino gerado e salvo!")

            treino_tabela = {"Dia": dias_semana}
            for grupo in grupos:
                treino_tabela[grupo] = [", ".join(treino[dia][grupo]) for dia in dias_semana]

            df_treino = pd.DataFrame(treino_tabela)
            st.table(df_treino)

    elif menu == "Histórico de Treinos":
        st.title("📜 Histórico de Treinos")
        treinos_agrupados = listar_treinos(usuario_id)

        if not treinos_agrupados:
            st.write("Nenhum treino encontrado.")
        else:
            for data, df_treino in treinos_agrupados.items():
                st.subheader(f"Treino gerado em: {data}")
                st.table(df_treino)

                if st.button(f"🗑 Deletar treino {data}", key=f"del_{data}"):
                    deletar_treino(data, usuario_id)
                    st.success(f"Treino de {data} removido com sucesso!")
                    st.rerun()
