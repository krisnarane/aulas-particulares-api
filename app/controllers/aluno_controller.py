from app.models.aluno import carregar_alunos


class AlunoController:
    def __init__(self):
        self._alunos = carregar_alunos()

    def _para_dicionario(self, aluno):
        return {
            "id": aluno.mostrar_id(),
            "nome": aluno.mostrar_nome(),
            "email": aluno.mostrar_email(),
            "perfil": aluno.mostrar_perfil(),
            "nivel": aluno.mostrar_nivel(),
            "aulas_agendadas": len(aluno.aulas_ativas()),
            "limite_aulas": aluno.mostrar_limite_aulas(),
        }

    # usados por outros controllers
    def todos(self):
        return list(self._alunos)

    def obter(self, id):
        return next((a for a in self._alunos if a.mostrar_id() == id), None)

    # casos de uso
    def buscar(self, id):
        aluno = self.obter(id)
        if aluno is None:
            return None
        return self._para_dicionario(aluno)


aluno_controller = AlunoController()
