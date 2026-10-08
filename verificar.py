"""Checagens automáticas do projeto. Rode com: python verificar.py"""

from pathlib import Path

from app.models.aluno import Aluno
from app.models.aula import Aula
from app.models.pessoa import Pessoa
from app.models.professor import PERFIS, Professor, ProfessorEspecialista

RAIZ = Path(__file__).parent
resultados = []


def checar(descricao, condicao):
    resultados.append(condicao)
    print(f"[{'OK' if condicao else 'FALHOU'}] {descricao}")


def lanca_value_error(funcao):
    try:
        funcao()
    except ValueError:
        return True
    return False


def arquivos_python(pasta):
    return list((RAIZ / pasta).rglob("*.py"))


# objetos novos, só para os testes (não mexem nos dados da API)
def novo_aluno(id=100):
    return Aluno(id, "Aluno Teste", "teste@email.com", "medio")


def novo_professor(id=100, valor=100):
    return Professor(id, "Prof Teste", "prof@email.com", "Matemática", valor)


def novo_especialista(id=101, valor=100):
    return ProfessorEspecialista(id, "Esp Teste", "esp@email.com", "Física", valor, "mestre")


print("=== Encapsulamento e regras de negócio ===")
checar("nome com menos de 3 letras é recusado",
       lanca_value_error(lambda: Aluno(1, "Al", "a@email.com", "medio")))
checar("e-mail sem @ é recusado",
       lanca_value_error(lambda: Aluno(1, "Alice", "alice.email.com", "medio")))
checar("nível de aluno inexistente é recusado",
       lanca_value_error(lambda: Aluno(1, "Alice", "a@email.com", "doutorado")))
checar("valor da hora fora da faixa é recusado",
       lanca_value_error(lambda: Professor(1, "Bruno", "b@email.com", "Inglês", -50)))
checar("aula fora do horário de funcionamento é recusada",
       lanca_value_error(lambda: Aula(1, novo_aluno(), novo_professor(), "2026-10-20", 21, 2)))
checar("aula com duração maior que 3 horas é recusada",
       lanca_value_error(lambda: Aula(1, novo_aluno(), novo_professor(), "2026-10-20", 10, 4)))
checar("data inválida é recusada",
       lanca_value_error(lambda: Aula(1, novo_aluno(), novo_professor(), "2026-02-30", 10, 1)))

prof = novo_professor()
Aula(1, novo_aluno(100), prof, "2026-10-20", 14, 2)
checar("professor não pode ter duas aulas sobrepostas",
       lanca_value_error(lambda: Aula(2, novo_aluno(101), prof, "2026-10-20", 15, 1)))

aula = Aula(3, novo_aluno(102), novo_professor(102), "2026-10-21", 9, 1)
aula.cancelar()
checar("aula já cancelada não pode ser cancelada de novo", lanca_value_error(aula.cancelar))

aluno_lotado = novo_aluno(103)
for dia in range(1, Aluno.LIMITE_AULAS + 1):
    Aula(10 + dia, aluno_lotado, novo_professor(200 + dia), f"2026-11-0{dia}", 10, 1)
checar("aluno não passa do LIMITE_AULAS",
       lanca_value_error(lambda: Aula(99, aluno_lotado, novo_professor(299), "2026-11-09", 10, 1)))

checar("atributos são todos protegidos (começam com _)",
       all(nome.startswith("_") for obj in (novo_aluno(), novo_especialista())
           for nome in vars(obj)))
checar("nenhuma classe tem alterar_id",
       not any(hasattr(c, "alterar_id") for c in (Pessoa, Aluno, Professor, ProfessorEspecialista, Aula)))

print("\n=== Herança e polimorfismo ===")
checar("hierarquia Pessoa -> Professor -> ProfessorEspecialista (2 níveis)",
       issubclass(ProfessorEspecialista, Professor) and issubclass(Professor, Pessoa)
       and issubclass(Aluno, Pessoa))
checar("valor_aula do especialista estende o do professor com super()",
       novo_especialista(valor=100).valor_aula(2) == novo_professor(valor=100).valor_aula(2)
       + 2 * ProfessorEspecialista.ADICIONAL_POR_HORA)
checar("permissoes() acumula as da classe mãe",
       set(novo_professor().permissoes()) < set(novo_especialista().permissoes()))
checar("LIMITE_AULAS tem valor diferente em cada filha",
       len({Aluno.LIMITE_AULAS, Professor.LIMITE_AULAS, ProfessorEspecialista.LIMITE_AULAS}) == 3)
checar("PERFIS mapeia o texto do mock para a classe",
       PERFIS == {"professor": Professor, "especialista": ProfessorEspecialista})
checar("aula com um aluno no lugar do professor é recusada (permissão, não tipo)",
       lanca_value_error(lambda: Aula(1, novo_aluno(1), novo_aluno(2), "2026-10-20", 10, 1)))

print("\n=== Camadas ===")
checar("nenhum import do FastAPI em app/models",
       not any("fastapi" in arq.read_text(encoding="utf-8").lower() for arq in arquivos_python("app/models")))
checar("nenhum import em app/data",
       not any("import" in arq.read_text(encoding="utf-8") for arq in arquivos_python("app/data")))
proibidos = ("isinstance(", "type(", "__class__", "__name__")
checar("nenhum if de tipo ou nome de classe no projeto",
       not any(p in arq.read_text(encoding="utf-8")
               for arq in arquivos_python("app") + [RAIZ / "main.py"] for p in proibidos))

print("\n=== Controllers ===")
from app.controllers.aula_controller import aula_controller          # noqa: E402
from app.controllers.professor_controller import professor_controller  # noqa: E402

checar("professor inexistente devolve None", professor_controller.buscar(999) is None)
matematica = professor_controller.listar_por_materia("matemática")
checar("filtro por matéria devolve só aquela matéria",
       len(matematica) == 2 and all(p["materia"] == "Matemática" for p in matematica))
checar("aulas de aluno inexistente devolve None", aula_controller.aulas_do_aluno(999) is None)
checar("faturamento soma só as aulas agendadas (R$ 840,00 nos mocks)",
       aula_controller.faturamento()["total"] == 840.0)

print("\n=== Rotas ===")
from main import app  # noqa: E402

esperadas = {
    ("GET", "/api/professores"),
    ("GET", "/api/professores/{id}"),
    ("GET", "/api/professores/materia/{materia}"),
    ("POST", "/api/aulas"),
    ("POST", "/api/aulas/{id}/cancelar"),
    ("GET", "/api/alunos/{id}/aulas"),
    ("GET", "/api/relatorio/faturamento"),
}
registradas = {(metodo.upper(), caminho)
               for caminho, metodos in app.openapi()["paths"].items() for metodo in metodos}
checar("as 7 rotas aparecem no /docs", esperadas == registradas)

total, passaram = len(resultados), sum(resultados)
print(f"\n{passaram}/{total} checagens passaram.")
raise SystemExit(0 if passaram == total else 1)
