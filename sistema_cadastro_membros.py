import csv

class SistemaCadastroMembros:
    def __init__(self, membros_file, advertencias_file):
        self.membros_file = membros_file
        self.advertencias_file = advertencias_file
        self.membros = self._carregar_membros()
        self.advertencias = self._carregar_advertencias()

    def _carregar_membros(self):
        membros = {}
        with open(self.membros_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                membros[row['nome']] = Membro(row['nome'], row['setor'], row['cargo'], int(row['pontos']))
        return membros

    def _carregar_advertencias(self):
        advertencias = []
        with open(self.advertencias_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                membro = self.membros[row['nome']]
                adv = Advertencia(membro, int(row['pontos']), row['motivo'])
                membro.adicionar_advertencia(adv)
                advertencias.append(adv)
        return advertencias

    def _salvar_membros(self):
        with open(self.membros_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nome', 'setor', 'cargo', 'pontos'])
            for membro in self.membros.values():
                writer.writerow([membro.nome, membro.setor, membro.cargo, membro.pontos])

    def _salvar_advertencias(self):
        with open(self.advertencias_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nome', 'pontos', 'motivo'])
            for adv in self.advertencias:
                writer.writerow([adv.membro.nome, adv.pontos, adv.motivo])

    def cadastrar_membro(self, nome, setor, cargo, pontos):
        if nome in self.membros:
            raise ValueError('Membro já cadastrado')
        self.membros[nome] = Membro(nome, setor, cargo, pontos)
        self._salvar_membros()

    def cadastrar_advertencia(self, nome_membro, pontos, motivo):
        membro = self.membros.get(nome_membro)
        if not membro:
            raise ValueError('Membro não encontrado')
        adv = Advertencia(membro, pontos, motivo)
        membro.adicionar_advertencia(adv)
        self.advertencias.append(adv)
        self._salvar_advertencias()

    def buscar_membro_por_nome(self, nome):
        membro = self.membros.get(nome)
        if not membro:
            raise ValueError('Membro não encontrado')
        return membro

    def buscar_advertencias_por_nome(self, nome):
        membro = self.membros.get(nome)
        if not membro:
            raise ValueError('Membro não encontrado')
        return membro.advertencias

class Membro:
    def __init__(self, nome, setor, cargo, pontos):
        self.nome = nome
        self.setor = setor
        self.cargo = cargo
        self.pontos = pontos
        self.advertencias = []

    def adicionar_advertencia(self, adv):
        self.advertencias.append(adv)
        self.pontos += adv.pontos

class Advertencia:
    def __init__(self, membro, pontos, motivo):
        self.membro = membro
        self.pontos = pontos
        self.motivo = motivo

    def __str__(self):
        return f'Advertência - Membro: {self.membro.nome} - Pontos: {self.pontos} - Motivo: {self.motivo}'

