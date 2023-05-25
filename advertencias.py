import csv

class AdvertenciasCSV:
    def read(advertencias_file, membros):
        advertencias = []
        with open(advertencias_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                membro = membros[row['nome']]
                adv = Advertencia(membro, int(row['pontos']), row['motivo'])
                membro.adicionar_advertencia(adv)
                advertencias.append(adv)
        return advertencias

    def save(advertencias_file, advertencias):
        with open(advertencias_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nome', 'pontos', 'motivo'])
            for adv in advertencias:
                writer.writerow([adv.membro.nome, adv.pontos, adv.motivo])

class Advertencia:
    def __init__(self, membro, pontos, motivo):
        self.membro = membro
        self.pontos = pontos
        self.motivo = motivo

    def __str__(self):
        return f'Advertência - Membro: {self.membro.nome} - Pontos: {self.pontos} - Motivo: {self.motivo}'