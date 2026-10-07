from datetime import datetime

from app.data.aulas_mock import AULAS


class Aula:
    """Registro que liga um Aluno a um Professor em uma data e horário."""

    HORA_ABERTURA = 7       # primeira aula começa às 7h
    HORA_FECHAMENTO = 22    # última aula termina até as 22h
    DURACAO_MAXIMA = 3      # em horas
    STATUS_VALIDOS = ("agendada", "cancelada")

    def __init__(self, id, aluno, professor, data, hora, duracao):
        # Permissão em vez de tipo: quem não tem "dar_aula" não pode ser o professor.
        if not aluno.tem_permissao("agendar_aula"):
            raise ValueError(f"{aluno.mostrar_nome()} não tem permissão para agendar aula.")
        if not professor.tem_permissao("dar_aula"):
            raise ValueError(f"{professor.mostrar_nome()} não tem permissão para dar aula.")

        self._id = id
        self._aluno = aluno
        self._professor = professor
        self.alterar_status("agendada")
        self.alterar_horario(data, hora, duracao)

        aluno.verificar_limite()
        professor.verificar_limite()
        aluno.vincular_aula(self)
        professor.vincular_aula(self)

    # ---------- leituras ----------
    def mostrar_id(self):
        return self._id

    def mostrar_aluno(self):
        return self._aluno

    def mostrar_professor(self):
        return self._professor

    def mostrar_data(self):
        return self._data

    def mostrar_hora(self):
        return self._hora

    def mostrar_hora_fim(self):
        return self._hora + self._duracao

    def mostrar_duracao(self):
        return self._duracao

    def mostrar_status(self):
        return self._status

    # ---------- alterações com regra ----------
    def alterar_status(self, status):
        if status not in self.STATUS_VALIDOS:
            raise ValueError(f"Status inválido. Use um destes: {', '.join(self.STATUS_VALIDOS)}.")
        self._status = status

    def alterar_horario(self, data, hora, duracao):
        """Define (ou remarca) o horário da aula."""
        if not self.esta_ativa():
            raise ValueError("Aula cancelada não pode ser remarcada.")
        try:
            datetime.strptime(str(data), "%Y-%m-%d")
        except ValueError:
            raise ValueError("A data precisa estar no formato AAAA-MM-DD e existir no calendário.")
        hora = int(hora)
        duracao = int(duracao)
        if duracao < 1 or duracao > self.DURACAO_MAXIMA:
            raise ValueError(f"A duração precisa ser de 1 a {self.DURACAO_MAXIMA} horas.")
        if hora < self.HORA_ABERTURA or hora + duracao > self.HORA_FECHAMENTO:
            raise ValueError(
                f"A aula precisa acontecer entre {self.HORA_ABERTURA}h e {self.HORA_FECHAMENTO}h."
            )
        self._aluno.verificar_disponibilidade(data, hora, duracao, ignorar=self)
        self._professor.verificar_disponibilidade(data, hora, duracao, ignorar=self)
        self._data = str(data)
        self._hora = hora
        self._duracao = duracao

    # ---------- comportamento ----------
    def esta_ativa(self):
        return self._status == "agendada"

    def sobrepoe(self, data, hora, duracao):
        """True se o intervalo informado bate com o horário desta aula."""
        return (
            self._data == data
            and hora < self._hora + self._duracao
            and self._hora < hora + duracao
        )

    def cancelar(self):
        if not self.esta_ativa():
            raise ValueError("Essa aula já está cancelada.")
        self.alterar_status("cancelada")

    def valor(self):
        # Polimorfismo: cada tipo de professor sabe calcular o próprio valor.
        return self._professor.valor_aula(self._duracao)

    def __repr__(self):
        return (
            f"Aula(id={self._id}, aluno='{self._aluno.mostrar_nome()}', "
            f"professor='{self._professor.mostrar_nome()}', data='{self._data}', "
            f"hora={self._hora}, duracao={self._duracao}, status='{self._status}')"
        )


def carregar_aulas(alunos, professores):
    alunos_por_id = {aluno.mostrar_id(): aluno for aluno in alunos}
    professores_por_id = {professor.mostrar_id(): professor for professor in professores}
    aulas = []
    for registro in AULAS:
        aula = Aula(
            registro["id"],
            alunos_por_id[registro["id_aluno"]],
            professores_por_id[registro["id_professor"]],
            registro["data"],
            registro["hora"],
            registro["duracao"],
        )
        if registro["status"] == "cancelada":
            aula.cancelar()
        aulas.append(aula)
    return aulas
