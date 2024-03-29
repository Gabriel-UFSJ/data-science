import streamlit as st
import csv

from agenda import Agenda
from sistema_cadastro_membros import SistemaCadastroMembros


USUARIOS_FILE = 'usuarios.csv'
MEMBROS_FILE = 'membros.csv'
ADVERTENCIAS_FILE = 'advertencias.csv'

class SistemaLogin:
    def __init__(self, usuarios_file):
        self.usuarios_file = usuarios_file
        
    def autenticar(self, username, senha):
        with open(self.usuarios_file, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if row[0] == username and row[1] == senha:
                    return row[2]  # retorna o tipo de usuário
        return None

    def logout(self):
        del st.session_state['username']
        del st.session_state['senha']

    def get_tipo_usuario(self, username):
        with open(self.usuarios_file, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if row[0] == username:
                    return row[2]
        return None

    def tipo_usuario(self):
        return st.session_state.get('tipo_usuario')

sistema_login = SistemaLogin(USUARIOS_FILE)
sistema_membros = SistemaCadastroMembros(MEMBROS_FILE, ADVERTENCIAS_FILE)

#Membros

def cadastrar_membro(sistema_membros):
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para cadastrar um membro.')
        return
    nome = st.text_input('Nome')
    email = st.text_input('Email')
    setor = st.text_input('Setor')
    cargo = st.text_input('Cargo')
    pontos = st.number_input('Pontos', value=0)
    if st.button('Cadastrar'):
        if sistema_membros.cadastrar_membro(nome, email, setor, cargo, pontos):
            st.success('Membro cadastrado com sucesso!')
        else:
            st.error('Membro já cadastrado')

def buscar_membro(sistema_membros):
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para cadastrar um membro.')
        return
    nome = st.text_input('Nome')
    if st.button('Buscar'):
        membro = sistema_membros.buscar_membro_por_nome(nome)
        if membro is None:
            st.error("Membro não encontrado")

        st.write(f'Nome: {membro.nome}')
        st.write(f'Email: {membro.email}')
        st.write(f'Setor: {membro.setor}')
        st.write(f'Cargo: {membro.cargo}')
        st.write(f'Pontos: {membro.pontos}')

def editar_membro(sistema_membros):
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para editar um membro.')
        return
    nome = st.text_input('Nome')
    setor_novo = st.text_input('Novo setor')
    cargo_novo = st.text_input('Novo cargo')
    pontos_novos = st.number_input('Novos pontos', value=0)
    if st.button('Editar'):
        try:
            sistema_membros.editar_membro(nome, setor_novo, cargo_novo, pontos_novos)
            st.success('Membro editado com sucesso!')
        except ValueError as e:
            st.error(str(e))            

def excluir_membro(sistema_membros):
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para excluir um membro.')
        return
    nome = st.text_input('Nome do membro a ser excluído')
    if st.button('Excluir'):
        if sistema_membros.excluir_membro(nome):
            st.success('Membro excluído com sucesso!')
        else:
            st.error('Membro não encontrado')

def listar_membros(sistema_membros):
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para listar os membros.')
        return
    st.write('Lista de membros')
    membros_selecionados = []
    for membro in sistema_membros.listar_membros():
        checkbox = st.checkbox(membro.nome)
        st.write(f'Email: {membro.email}', f'Setor: {membro.setor}', f'Cargo: {membro.cargo}', f'Pontos: {membro.pontos}')
        if checkbox:
            membros_selecionados.append(membro)
    return membros_selecionados
    
# Advertências

def cadastrar_advertencia(sistema_membros):
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para cadastrar uma advertência.')
        return
    nome_membro = st.text_input('Nome do membro')
    pontos = st.number_input('Pontos', value=0)
    motivo = st.text_input('Motivo')
    if st.button('Cadastrar'):
        membro = sistema_membros.buscar_membro_por_nome(nome_membro)
        if membro is None:
            st.error("Membro não encontrado")

        sistema_membros.cadastrar_advertencia(membro, pontos, motivo)
        st.success('Advertência cadastrada com sucesso!')

def editar_advertencia(sistema_membros):
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para editar uma advertência.')
        return
    nome_membro = st.text_input('Nome do membro')
    indice_advertencia = st.number_input('Índice da advertência', value=0)
    pontos_novos = st.number_input('Novos pontos', value=0)
    motivo_novo = st.text_input('Novo motivo')
    if st.button('Editar'):
        try:
            sistema_membros.editar_advertencia(nome_membro, indice_advertencia, pontos_novos, motivo_novo)
            st.success('Advertência editada com sucesso!')
        except ValueError as e:
            st.error(str(e))

def excluir_advertencia(sistema_membros):
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para excluir uma advertência.')
        return
    
    nome_membro = st.text_input('Nome do membro')
    if st.button('Pesquisar Membro'):
        advertencias = sistema_membros.buscar_advertencias_por_nome(nome_membro)

        if len(advertencias) > 0:
            st.write('Advertências encontradas:')
            for i, adv in enumerate(advertencias):
                st.write(f'{i + 1}. {str(adv)}')
            index = st.number_input('Selecione o número da advertência a ser excluída', value=1, min_value=1,
                                    max_value=len(advertencias), step=1)
            if st.button('Excluir'):
                try:
                    sistema_membros.excluir_advertencia(nome_membro, index - 1)
                    st.success('Advertência excluída com sucesso!')
                except ValueError as e:
                    st.error(str(e))
        else:
            st.warning('Nenhuma advertência encontrada para o membro especificado.')

def buscar_advertencias(sistema_membros):
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para buscar advertências.')
        return
    nome = st.text_input('Nome')
    if st.button('Buscar'):
        advertencias = sistema_membros.buscar_advertencias_por_nome(nome)
        if advertencias is None:
            st.error("Membro não encontrado")

        for adv in advertencias:
            st.write(str(adv))

def criar_reuniao(agenda):
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para listar os membros.')
        return
    
    with st.form("my_form"):
        data = st.text_input("Data da reunião: ")
        horario = st.text_input("Horário da reunião: ")
        local = st.text_input("Local da reunião: ")
        assunto = st.text_input("Assunto da reunião: ")

        st.write('Lista de membros')

        membros = sistema_membros.listar_membros()
        membros_selecionados = st.multiselect("Selecione os membros", membros, format_func=lambda membro: membro.nome)

        submitted = st.form_submit_button("Submit")
        if submitted:
            agenda.criar_reuniao(data, horario, local, assunto, membros_selecionados)
            st.success('Reunião cadastrada com sucesso!')

def main():
    sistema_login = SistemaLogin(USUARIOS_FILE)
    sistema_membros = SistemaCadastroMembros(MEMBROS_FILE, ADVERTENCIAS_FILE)
    agenda = Agenda()

    # Verifica se o usuário está autenticado
    if 'username' in st.session_state:
        # Obtém o tipo de usuário a partir do CSV
        tipo_usuario = sistema_login.autenticar(st.session_state['username'], st.session_state['senha'])

        # Verifica se o usuário ainda existe no CSV, caso contrário faz logout
        if tipo_usuario is None:
            sistema_login.logout()
        else:
            st.sidebar.title(f"Olá, {st.session_state['username']}!")
            st.sidebar.write("Você está autenticado.")
            st.sidebar.button('Logout', on_click=sistema_login.logout)

            if tipo_usuario == 'administrador':
                # Opções do menu para administradores
                opcoes = ['Cadastrar Membro', 'Editar Membro', 'Excluir Membro',
                        'Cadastrar Advertência', 'Editar Advertência', 'Excluir Advertência',
                        'Buscar Membro', 'Buscar Advertências', 'Criar Reunião']
            else:
                # Opções do menu para membros comuns
                opcoes = ['Cadastrar Membro', 'Buscar Membro', 'Buscar Advertências']

            escolha = st.sidebar.selectbox('Escolha uma opção', opcoes)
            if escolha == 'Cadastrar Membro':
                cadastrar_membro(sistema_membros)
            elif escolha == 'Editar Membro':
                editar_membro(sistema_membros)
            elif escolha == 'Excluir Membro':
                excluir_membro(sistema_membros)
            elif escolha == 'Cadastrar Advertência':
                cadastrar_advertencia(sistema_membros)
            elif escolha == 'Editar Advertência':
                editar_advertencia(sistema_membros)
            elif escolha == 'Excluir Advertência':
                excluir_advertencia(sistema_membros)
            elif escolha == 'Buscar Membro':
                buscar_membro(sistema_membros)
            elif escolha == 'Buscar Advertências':
                buscar_advertencias(sistema_membros)
            elif escolha == 'Criar Reunião':
                criar_reuniao(agenda)

    else:
        st.title('Sistema de Cadastro de Membros e Advertências')
        st.write('Por favor, faça o login:')
        username = st.text_input('Username')
        senha = st.text_input('Senha', type='password')

        if st.button('Login'):
            tipo_usuario = sistema_login.autenticar(username, senha)
            if tipo_usuario is not None:
                st.session_state['username'] = username
                st.session_state['senha'] = senha
                st.session_state['tipo_usuario'] = tipo_usuario
            else:
                st.error('Usuário ou senha inválidos.')

if __name__ == '__main__':
    main()

