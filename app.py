import streamlit as st
import csv
from sistema_cadastro_membros import SistemaCadastroMembros

USUARIOS_FILE = 'usuarios.csv'
MEMBROS_FILE = 'membros.csv'
ADVERTENCIAS_FILE = 'advertencias.csv'

sistema = SistemaCadastroMembros(MEMBROS_FILE, ADVERTENCIAS_FILE)

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
        if 'username' in st.session_state:
            del st.session_state['username']
            del st.session_state['senha']
        else:
            st.warning('Usuário não está logado.')
    
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

def cadastrar_membro():
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para cadastrar uma advertência.')
        return
    nome = st.text_input('Nome')
    email = st.text_input('Email')
    setor = st.text_input('Setor')
    cargo = st.text_input('Cargo')
    pontos = st.number_input('Pontos', value=0)
    if st.button('Cadastrar'):
        if sistema.cadastrar_membro(nome, email, setor, cargo, pontos):
            st.success('Membro cadastrado com sucesso!')
        else:
            st.error('Membro já cadastrado')

def editar_membro():
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para editar um membro.')
        return
    nome = st.text_input('Nome')
    setor_novo = st.text_input('Novo setor')
    cargo_novo = st.text_input('Novo cargo')
    pontos_novos = st.number_input('Novos pontos', value=0)
    if st.button('Editar'):
        try:
            sistema.editar_membro(nome, setor_novo, cargo_novo, pontos_novos)
            st.success('Membro editado com sucesso!')
        except ValueError as e:
            st.error(str(e))            

def excluir_membro():
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para excluir um membro.')
        return
    nome = st.text_input('Nome do membro a ser excluído')
    if st.button('Excluir'):
        try:
            sistema.excluir_membro(nome)
            st.success('Membro excluído com sucesso!')
        except ValueError as e:
            st.error(str(e))

def cadastrar_advertencia():
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para cadastrar uma advertência.')
        return
    nome_membro = st.text_input('Nome do membro')
    pontos = st.number_input('Pontos', value=0)
    motivo = st.text_input('Motivo')
    if st.button('Cadastrar'):
        membro = sistema.buscar_membro_por_nome(nome_membro)
        if membro is None:
            st.error("Membro não encontrado")

        sistema.cadastrar_advertencia(membro, pontos, motivo)
        st.success('Advertência cadastrada com sucesso!')

def editar_advertencia():
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para editar uma advertência.')
        return
    nome_membro = st.text_input('Nome do membro')
    pontos_antigos = st.number_input('Pontos antigos', value=0)
    pontos_novos = st.number_input('Novos pontos', value=0)
    motivo_novo = st.text_input('Novo motivo')
    if st.button('Editar'):
        try:
            sistema.editar_advertencia(nome_membro, pontos_antigos, pontos_novos, motivo_novo)
            st.success('Advertência editada com sucesso!')
        except ValueError as e:
            st.error(str(e))


def excluir_advertencia():
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para excluir uma advertência.')
        return
    nome_membro = st.text_input('Nome do membro')
    pontos = st.number_input('Pontos', value=0)
    motivo = st.text_input('Motivo')
    if st.button('Excluir'):
        try:
            sistema.excluir_advertencia(nome_membro, pontos, motivo)
            st.success('Advertência excluída com sucesso!')
        except ValueError as e:
            st.error(str(e))

def buscar_membro():
    if not st.session_state.get('está logado'):
        st.error('Você precisa fazer login para buscar um membro.')
        return
    nome = st.text_input('Nome')
    if st.button('Buscar'):
        membro = sistema.buscar_membro_por_nome(nome)
        if membro is None:
            st.error("Membro não encontrado")

        st.write(f'Nome: {membro.nome}')
        st.write(f'Email: {membro.email}')
        st.write(f'Setor: {membro.setor}')
        st.write(f'Cargo: {membro.cargo}')
        st.write(f'Pontos: {membro.pontos}')

def buscar_advertencias():
    if 'username' not in st.session_state:
        st.error('Você precisa fazer login para cadastrar uma advertência.')
        return
    nome = st.text_input('Nome')
    if st.button('Buscar'):
        advertencias = sistema.buscar_advertencias_por_nome(nome)
        if advertencias is None:
            st.error("Membro não encontrado")

        for adv in advertencias:
            st.write(str(adv))

def main():
    sistema_login = SistemaLogin(USUARIOS_FILE)

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
                opcoes = ['Cadastrar Membro', 'Cadastrar Advertência', 'Buscar Membro', 'Buscar Advertências']
            else:
                # Opções do menu para membros comuns
                opcoes = ['Buscar Membro', 'Buscar Advertências']

            escolha = st.sidebar.selectbox('Escolha uma opção', opcoes)

            # Opções que só podem ser acessadas por administradores
            if escolha == 'Cadastrar Membro' and tipo_usuario == 'administrador':
                cadastrar_membro()
            elif escolha == 'Cadastrar Advertência' and tipo_usuario == 'administrador':
                cadastrar_advertencia()
            elif escolha == 'Editar Membro' and tipo_usuario == 'administrador':
                editar_membro()
            elif escolha == 'Excluir Membro' and tipo_usuario == 'administrador':
                excluir_membro()
            elif escolha == 'Editar Advertência' and tipo_usuario == 'administrador':
                editar_advertencia()
            elif escolha == 'Excluir Advertência' and tipo_usuario == 'administrador':
                excluir_advertencia()

            # Opções que podem ser acessadas por ambos os tipos de usuário
            elif escolha == 'Buscar Membro':
                buscar_membro()
            elif escolha == 'Buscar Advertências':
                buscar_advertencias()
    else:
        # Mostra a página de login
        st.title('Sistema de Gerenciamento de Membros')
        st.write('Faça login para continuar.')
        username = st.text_input('Usuário')
        senha = st.text_input('Senha', type='password')
        if st.button('Login'):
            tipo_usuario = sistema_login.autenticar(username, senha)
            if tipo_usuario is not None:
                st.session_state['username'] = username
                st.session_state['senha'] = senha
                st.session_state['está logado'] = True
            else:
                st.error('Usuário ou senha incorretos.')

if __name__ == '__main__':
    main()