import streamlit as st
from sistema_cadastro_membros import Membro, SistemaCadastroMembros

sistema = SistemaCadastroMembros("membros.csv")

st.title("Sistema de Cadastro de Membros")

nome = st.text_input("Nome do Membro:")

setores = ["Powertrain", "Simulação", "Sistemas Elétricos", "Comercial","Engenharia do Produto","Estrutura e Aerodinâmica","Direção e Frenagem"]
setor = st.selectbox("Setor do Membro:", setores)

cargos = ["Trainee", "Membro Efetivo", "Diretoria", "Capitania"]
cargo = st.selectbox("Cargo do Membro:", cargos)

if st.button("Adicionar Membro"):
    sistema.cadastrar_membro(nome, setor, cargo)
    st.success("Membro adicionado com sucesso!")

st.header("Gerenciamento de Membros")

if st.button("Listar Membros"):
    st.write("Lista de Membros:")
    for membro in sistema.membros:
        st.write(f"- {membro.nome} ({membro.setor}, {membro.cargo}, {membro.pontos} pontos)")

buscar_nome = st.text_input("Buscar Membro pelo nome:")
if st.button("Buscar"):
    membro = sistema.encontrar_membro_por_nome(buscar_nome)
    if membro:
        st.write(f"Membro encontrado: {membro.nome} ({membro.setor}, {membro.cargo}, {membro.pontos} pontos)")
    else:
        st.warning("Membro não encontrado.")

membros_nomes = [membro.nome for membro in sistema.membros]
membro_selecionado = st.selectbox("Selecione o Membro:", membros_nomes)

quantidade = st.number_input("Quantidade de Pontos:", min_value=1, step=1)

if st.button("Aplicar Advertência"):
    membro = sistema.encontrar_membro_por_nome(membro_selecionado)
    if membro:
        membro.aplicar_advertencia(quantidade)
        sistema.salvar_membros()
        st.success(f"Advertência de {quantidade} pontos aplicada a {membro.nome} ({membro.setor}, {membro.cargo}).")
    else:
        st.error("Membro não encontrado.")
