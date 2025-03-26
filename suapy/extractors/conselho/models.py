class Turma:
    def __init__(self, codigo: str):
        self.codigo = codigo
        self.componentes = []
        self.estudantes = []
    
    def adicionar_componente(self, componente):
        self.componentes.append(componente)
    
    def adicionar_estudante(self, estudante):
        self.estudantes.append(estudante)

class ComponenteCurricular:
    def __init__(self, nome: str, docente: str, aulas_semanais: int, aulas_totais: int, aulas_realizadas: int):
        self.nome = nome
        self.docente = docente
        self.aulas_semanais = aulas_semanais
        self.aulas_totais = aulas_totais
        self.aulas_realizadas = aulas_realizadas

class Estudante:
    def __init__(self, nome: str, matricula: str, situacao: str):
        self.nome = nome
        self.matricula = matricula
        self.situacao = situacao
        self.notas = {}
        self.faltas = {}
    
    def adicionar_notas(self, componente: str, n1: float, n2: float, n3: float, media: float):
        self.notas[componente] = {'N1': n1, 'N2': n2, 'N3': n3, 'Média': media}
    
    def adicionar_faltas(self, componente: str, faltas: int):
        self.faltas[componente] = faltas
