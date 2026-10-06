class Pessoa:
    """Base da hierarquia: o que aluno e professor têm em comum.

    Pessoa -> Aluno
    Pessoa -> Professor -> ProfessorEspecialista
    """

    # Constantes de classe: cada filha sobrescreve com o seu valor.
    PERFIL = "pessoa"
    LIMITE_AULAS = 0

    def __init__(self, id, nome, email):
        self._id = id          # sem alterar_id: o id nunca muda
        self._aulas = []       # aulas em que a pessoa participa
        self.alterar_nome(nome)
        self.alterar_email(email)

    # ---------- leituras ----------
    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def mostrar_email(self):
        return self._email

    def mostrar_perfil(self):
        return self.PERFIL

    def mostrar_limite_aulas(self):
        return self.LIMITE_AULAS

    def mostrar_aulas(self):
        return list(self._aulas)  # cópia: quem lê não altera a lista interna

    # ---------- alterações com regra ----------
    def alterar_nome(self, nome):
        nome = str(nome).strip()
        if len(nome) < 3:
            raise ValueError("O nome precisa ter pelo menos 3 letras.")
        self._nome = nome

    def alterar_email(self, email):
        email = str(email).strip().lower()
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("E-mail inválido.")
        self._email = email

    # ---------- permissões (as filhas estendem com super()) ----------
    def permissoes(self):
        return ["ver_professores"]

    def tem_permissao(self, permissao):
        return permissao in self.permissoes()

    # ---------- agenda ----------
    def aulas_ativas(self):
        return [aula for aula in self._aulas if aula.esta_ativa()]

    def esta_disponivel(self, data, hora, duracao, ignorar=None):
        conflitos = [
            aula for aula in self.aulas_ativas()
            if aula is not ignorar and aula.sobrepoe(data, hora, duracao)
        ]
        return len(conflitos) == 0

    def atingiu_limite(self):
        return len(self.aulas_ativas()) >= self.LIMITE_AULAS

    def verificar_disponibilidade(self, data, hora, duracao, ignorar=None):
        if not self.esta_disponivel(data, hora, duracao, ignorar):
            raise ValueError(f"{self._nome} já tem aula nesse horário.")

    def verificar_limite(self):
        if self.atingiu_limite():
            raise ValueError(
                f"{self._nome} atingiu o limite de {self.LIMITE_AULAS} aulas agendadas."
            )

    def vincular_aula(self, aula):
        self._aulas.append(aula)

    def __repr__(self):
        return f"Pessoa(id={self._id}, nome='{self._nome}')"
