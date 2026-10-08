from app.controllers.aluno_controller import aluno_controller
from app.controllers.professor_controller import professor_controller
from app.models.aula import Aula, carregar_aulas


class AulaController:
    def __init__(self, alunos, professores):
        self._alunos = alunos
        self._professores = professores
        self._aulas = carregar_aulas(alunos.todos(), professores.todos())

    def _para_dicionario(self, aula):
        aluno = aula.mostrar_aluno()
        professor = aula.mostrar_professor()
        return {
            "id": aula.mostrar_id(),
            "aluno": {"id": aluno.mostrar_id(), "nome": aluno.mostrar_nome()},
            "professor": {
                "id": professor.mostrar_id(),
                "nome": professor.mostrar_nome(),
                "perfil": professor.mostrar_perfil(),
                "materia": professor.mostrar_materia(),
            },
            "data": aula.mostrar_data(),
            "inicio": f"{aula.mostrar_hora():02d}:00",
            "fim": f"{aula.mostrar_hora_fim():02d}:00",
            "duracao_horas": aula.mostrar_duracao(),
            "status": aula.mostrar_status(),
            "valor": aula.valor(),
        }

    def _proximo_id(self):
        return max((a.mostrar_id() for a in self._aulas), default=0) + 1

    def _obter(self, id):
        return next((a for a in self._aulas if a.mostrar_id() == id), None)

    # ---------- casos de uso ----------
    def buscar(self, id):
        aula = self._obter(id)
        if aula is None:
            return None
        return self._para_dicionario(aula)

    def participantes_existem(self, id_aluno, id_professor):
        return (
            self._alunos.obter(id_aluno) is not None
            and self._professores.obter(id_professor) is not None
        )

    def horario_ocupado(self, id_aluno, id_professor, data, hora, duracao):
        """True se o pedido conflita com o estado atual da agenda (vira 409 na rota)."""
        aluno = self._alunos.obter(id_aluno)
        professor = self._professores.obter(id_professor)
        return (
            not aluno.esta_disponivel(data, hora, duracao)
            or not professor.esta_disponivel(data, hora, duracao)
            or aluno.atingiu_limite()
            or professor.atingiu_limite()
        )

    def agendar(self, id_aluno, id_professor, data, hora, duracao):
        aluno = self._alunos.obter(id_aluno)
        professor = self._professores.obter(id_professor)
        if aluno is None or professor is None:
            return None
        aula = Aula(self._proximo_id(), aluno, professor, data, hora, duracao)  # pode lançar ValueError
        self._aulas.append(aula)
        return self._para_dicionario(aula)

    def cancelar(self, id):
        aula = self._obter(id)
        if aula is None:
            return None
        aula.cancelar()  # pode lançar ValueError
        return self._para_dicionario(aula)

    def aulas_do_aluno(self, id_aluno):
        aluno = self._alunos.obter(id_aluno)
        if aluno is None:
            return None
        return [self._para_dicionario(a) for a in self._aulas if a.mostrar_aluno() is aluno]

    def faturamento(self):
        ativas = [a for a in self._aulas if a.esta_ativa()]
        por_professor = {}
        for aula in ativas:
            nome = aula.mostrar_professor().mostrar_nome()
            por_professor[nome] = por_professor.get(nome, 0) + aula.valor()
        return {
            "aulas_agendadas": len(ativas),
            "total": sum(aula.valor() for aula in ativas),
            "por_professor": por_professor,
        }


aula_controller = AulaController(aluno_controller, professor_controller)
