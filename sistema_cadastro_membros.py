import csv

class SistemaCadastroMembros:
    def __init__(self, arquivo_membros, arquivo_advertencias):
        self.arquivo_membros = arquivo_membros
        self.arquivo_advertencias = arquivo_advertencias
        self.membros = self.carregar_membros()
        self.advertencias = self.carregar_advertencias()

    def carregar_membros(self):
        membros = {}
        with open(self.arquivo_membros, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                membros[row['nome']] = Membro(row['nome'], row['setor'], row['cargo'], int(row['pontos']))
        return membros

    def carregar_advertencias(self):
        advertencias = []
        with open(self.arquivo_advertencias, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                nome_membro = row['nome']
                if nome_membro in self.membros:
                    membro = self.membros[nome_membro]
                    adv = Advertencia(membro, int(row['pontos']), row['motivo'])
                    membro.adicionar_advertencia(adv)
                    advertencias.append(adv)
        return advertencias

    def salvar_membros(self):
        with open(self.arquivo_membros, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nome', 'setor', 'cargo', 'pontos'])
            for membro in self.membros.values():
                writer.writerow([membro.nome, membro.setor, membro.cargo, membro.pontos])

    def salvar_advertencias(self):
        with open(self.arquivo_advertencias, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nome', 'pontos', 'motivo'])
            for adv in self.advertencias:
                writer.writerow([adv.membro.nome, adv.pontos, adv.motivo])

    def excluir_advertencias_do_membro(self, membro):
        advertencias_remanescentes = [adv for adv in self.advertencias if adv.membro != membro]
        self.advertencias = advertencias_remanescentes

    def cadastrar_membro(self, nome, setor, cargo, pontos):
        if nome in self.membros:
            raise ValueError('Membro já cadastrado')
        self.membros[nome] = Membro(nome, setor, cargo, pontos)
        self.salvar_membros()

    def editar_membro(self, nome, setor, cargo, pontos):
        membro = self.membros.get(nome)
        if not membro:
            raise ValueError('Membro não encontrado')
        membro.setor = setor
        membro.cargo = cargo
        membro.pontos = pontos
        self.salvar_membros()
    
    def excluir_membro(self, nome):
        membro = self.membros.get(nome)
        if not membro:
            raise ValueError('Membro não encontrado')
        del self.membros[nome]
        self.excluir_advertencias_do_membro(membro)
        self.salvar_membros()

    def cadastrar_advertencia(self, nome_membro, pontos, motivo):
        membro = self.membros.get(nome_membro)
        if not membro:
            raise ValueError('Membro não encontrado')
        adv = Advertencia(membro, pontos, motivo)
        membro.adicionar_advertencia(adv)
        self.advertencias.append(adv)
        self.salvar_advertencias()
    
    def editar_advertencia(self, nome_membro, indice_advertencia, pontos, motivo):
        advertencias = self.buscar_advertencias_por_nome(nome_membro)
        if indice_advertencia < 0 or indice_advertencia >= len(advertencias):
            raise ValueError('Índice de advertência inválido')
        advertencia = advertencias[indice_advertencia]
        advertencia.pontos = pontos
        advertencia.motivo = motivo
        self.salvar_advertencias()

    def excluir_advertencia(self, nome_membro, indice_advertencia):
        membro = self.membros.get(nome_membro)
        if not membro:
            return
        advertencias = membro.advertencias
        if indice_advertencia < 0 or indice_advertencia >= len(advertencias):
            raise ValueError('Índice de advertência inválido')
        advertencia = advertencias.pop(indice_advertencia)
        membro.pontos -= advertencia.pontos
        self.salvar_advertencias()

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
