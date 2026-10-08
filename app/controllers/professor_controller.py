from app.models.professor import carregar_professores


class ProfessorController:
    def __init__(self):
        self._professores = carregar_professores()

    def _para_dicionario(self, professor):
        return {
            "id": professor.mostrar_id(),
            "nome": professor.mostrar_nome(),
            "email": professor.mostrar_email(),
            "perfil": professor.mostrar_perfil(),
            "materia": professor.mostrar_materia(),
            "valor_hora_base": professor.mostrar_valor_hora(),
            "valor_uma_hora_de_aula": professor.valor_aula(1),
            "aulas_agendadas": len(professor.aulas_ativas()),
            "limite_aulas": professor.mostrar_limite_aulas(),
            "permissoes": professor.permissoes(),
        }

    # usados por outros controllers
    def todos(self):
        return list(self._professores)

    def obter(self, id):
        return next((p for p in self._professores if p.mostrar_id() == id), None)

    # casos de uso
    def listar(self):
        return [self._para_dicionario(p) for p in self._professores]

    def buscar(self, id):
        professor = self.obter(id)
        if professor is None:
            return None
        return self._para_dicionario(professor)

    def listar_por_materia(self, materia):
        materia = materia.strip().lower()
        return [
            self._para_dicionario(p)
            for p in self._professores
            if p.mostrar_materia().lower() == materia
        ]


professor_controller = ProfessorController()
