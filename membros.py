import csv

class MembrosCSV:
    def read(membros_file):
        membros = {}
        with open(membros_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                membros[row['nome']] = Membro(row['nome'], row['email'], row['setor'], row['cargo'], int(row['pontos']))
        return membros

    def save(membros, membros_file):
        with open(membros_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nome', 'email', 'setor', 'cargo', 'pontos'])
            for membro in membros.values():
                writer.writerow([membro.nome, membro.email, membro.setor, membro.cargo, membro.pontos])

class Membro:
    def __init__(self, nome, email, setor, cargo, pontos):
        self.nome = nome
        self.email = email
        self.setor = setor
        self.cargo = cargo
        self.pontos = pontos
        self.advertencias = []

    def adicionar_advertencia(self, adv):
        self.advertencias.append(adv)
        self.pontos += adv.pontos