from membros import MembrosCSV, Membro
from advertencias import AdvertenciasCSV, Advertencia

class SistemaCadastroMembros:
    def __init__(self, membros_file, advertencias_file):
        self.membros_file = membros_file
        self.advertencias_file = advertencias_file

        self.membros = MembrosCSV.read(self.membros_file)
        self.advertencias = AdvertenciasCSV.read(self.membros_file, self.membros)

    def _salvar_membros(self):
        MembrosCSV.save(self.membros, self.membros_file)

    def _salvar_advertencias(self):
        AdvertenciasCSV.save(self.membros_file, self.membros)

    def cadastrar_membro(self, nome, email, setor, cargo, pontos):
        if nome in self.membros:
            return False
        self.membros[nome] = Membro(nome, email, setor, cargo, pontos)
        self._salvar_membros()
        return True

    def editar_membro(self, nome, setor, cargo, pontos):
        membro = self.buscar_membro_por_nome(nome)
        if membro is None:
            return False

        membro.setor = setor
        membro.cargo = cargo
        membro.pontos = pontos
        self._salvar_membros()
        return True
    
    def excluir_membro(self, nome):
        if nome not in self.membros:
            return False
        
        del self.membros[nome]
        self._salvar_membros()
        return True

    def cadastrar_advertencia(self, membro, pontos, motivo):
        adv = Advertencia(membro, pontos, motivo)
        membro.adicionar_advertencia(adv)
        self.advertencias.append(adv)
        self._salvar_advertencias()
    
    def editar_advertencia(self, membro_nome, indice_advertencia, pontos, motivo):
        advertencias = self.buscar_advertencias_por_nome(membro_nome)
        if indice_advertencia < 0 or indice_advertencia >= len(advertencias):
            raise ValueError('Índice de advertência inválido')
        advertencia = advertencias[indice_advertencia]
        advertencia.pontos = pontos
        advertencia.motivo = motivo
        self._salvar_advertencias()

    def excluir_advertencia(self, membro_nome, indice_advertencia):
        advertencias = self.buscar_advertencias_por_nome(membro_nome)
        if indice_advertencia < 0 or indice_advertencia >= len(advertencias):
            raise ValueError('Índice de advertência inválido')
        
        advertencias.pop(indice_advertencia)
        self._salvar_advertencias()

    def buscar_membro_por_nome(self, nome):
        return self.membros.get(nome)

    def buscar_advertencias_por_nome(self, nome):
        membro = self.membros.get(nome)
        if not membro:
            return None
        return membro.advertencias
