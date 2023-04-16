import csv

class Membro:
    def __init__(self, nome, setor, cargo, pontos=0):
        self.nome = nome
        self.setor = setor
        self.cargo = cargo
        self.pontos = pontos

    def adicionar_pontos(self, quantidade):
        self.pontos += quantidade

    def aplicar_advertencia(self, quantidade):
        self.adicionar_pontos(quantidade)


class SistemaCadastroMembros:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.membros = self.carregar_membros()

    def cadastrar_membro(self, nome, setor, cargo, pontos=0):
        membro = Membro(nome, setor, cargo, pontos)
        self.membros.append(membro)
        self.salvar_membros()

    def encontrar_membro_por_nome(self, nome):
        for membro in self.membros:
            if membro.nome == nome:
                return membro
        return None

    def carregar_membros(self):
        membros = []
        try:
            with open(self.arquivo, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[3].isdigit():
                        membro = Membro(row[0], row[1], row[2], int(row[3]))
                        membros.append(membro)
        except FileNotFoundError:
            pass
        return membros


    def salvar_membros(self):
        with open(self.arquivo, "w", newline="") as f:
            writer = csv.writer(f)
            for membro in self.membros:
                writer.writerow([membro.nome, membro.setor, membro.cargo, membro.pontos])
    
    def buscar_membro_por_nome(self, nome):
        membro = self.encontrar_membro_por_nome(nome)
        if membro:
            return {"nome": membro.nome, "cargo": membro.cargo, "setor": membro.setor, "pontos": membro.pontos}
        else:
            return None