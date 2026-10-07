from app.data.professores_mock import PROFESSORES
from app.models.pessoa import Pessoa


class Professor(Pessoa):
    PERFIL = "professor"
    LIMITE_AULAS = 10
    VALOR_HORA_MINIMO = 20.0
    VALOR_HORA_MAXIMO = 500.0

    def __init__(self, id, nome, email, materia, valor_hora):
        super().__init__(id, nome, email)
        self.alterar_materia(materia)
        self.alterar_valor_hora(valor_hora)

    def mostrar_materia(self):
        return self._materia

    def mostrar_valor_hora(self):
        return self._valor_hora

    def alterar_materia(self, materia):
        materia = str(materia).strip()
        if not materia:
            raise ValueError("A matéria não pode ficar vazia.")
        self._materia = materia

    def alterar_valor_hora(self, valor_hora):
        valor_hora = float(valor_hora)
        if valor_hora < self.VALOR_HORA_MINIMO or valor_hora > self.VALOR_HORA_MAXIMO:
            raise ValueError(
                f"O valor da hora precisa estar entre R$ {self.VALOR_HORA_MINIMO:.2f} "
                f"e R$ {self.VALOR_HORA_MAXIMO:.2f}."
            )
        self._valor_hora = valor_hora

    def valor_aula(self, duracao):
        return self._valor_hora * duracao

    def permissoes(self):
        return super().permissoes() + ["dar_aula"]

    def __repr__(self):
        return f"Professor(id={self._id}, nome='{self._nome}', materia='{self._materia}')"


class ProfessorEspecialista(Professor):
    """Professor com pós-graduação: cobra um adicional por hora e tem agenda mais curta."""

    PERFIL = "especialista"
    LIMITE_AULAS = 6
    ADICIONAL_POR_HORA = 40.0
    TITULACOES = ("especialista", "mestre", "doutor")

    def __init__(self, id, nome, email, materia, valor_hora, titulacao):
        super().__init__(id, nome, email, materia, valor_hora)
        self.alterar_titulacao(titulacao)

    def mostrar_titulacao(self):
        return self._titulacao

    def alterar_titulacao(self, titulacao):
        titulacao = str(titulacao).strip().lower()
        if titulacao not in self.TITULACOES:
            raise ValueError(f"Titulação inválida. Use uma destas: {', '.join(self.TITULACOES)}.")
        self._titulacao = titulacao

    def valor_aula(self, duracao):
        # aproveita o cálculo do Professor e soma o adicional
        return super().valor_aula(duracao) + self.ADICIONAL_POR_HORA * duracao

    def permissoes(self):
        return super().permissoes() + ["preparar_vestibular"]

    def __repr__(self):
        return (
            f"ProfessorEspecialista(id={self._id}, nome='{self._nome}', "
            f"materia='{self._materia}', titulacao='{self._titulacao}')"
        )


# Texto do mock -> classe. É isso que evita um if comparando o perfil.
PERFIS = {
    "professor": Professor,
    "especialista": ProfessorEspecialista,
}


def carregar_professores():
    professores = []
    for registro in PROFESSORES:
        classe = PERFIS[registro["perfil"]]
        dados = {chave: valor for chave, valor in registro.items() if chave != "perfil"}
        professores.append(classe(**dados))
    return professores
