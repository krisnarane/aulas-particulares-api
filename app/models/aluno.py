from app.data.alunos_mock import ALUNOS
from app.models.pessoa import Pessoa


class Aluno(Pessoa):
    PERFIL = "aluno"
    LIMITE_AULAS = 4  # aluno pode ter no máximo 4 aulas agendadas ao mesmo tempo
    NIVEIS = ("fundamental", "medio", "superior", "adulto")

    def __init__(self, id, nome, email, nivel):
        super().__init__(id, nome, email)
        self.alterar_nivel(nivel)

    def mostrar_nivel(self):
        return self._nivel

    def alterar_nivel(self, nivel):
        nivel = str(nivel).strip().lower()
        if nivel not in self.NIVEIS:
            raise ValueError(f"Nível inválido. Use um destes: {', '.join(self.NIVEIS)}.")
        self._nivel = nivel

    def permissoes(self):
        # estende a lista da Pessoa em vez de reescrevê-la
        return super().permissoes() + ["agendar_aula", "cancelar_aula"]

    def __repr__(self):
        return f"Aluno(id={self._id}, nome='{self._nome}', nivel='{self._nivel}')"


def carregar_alunos():
    return [Aluno(**registro) for registro in ALUNOS]
