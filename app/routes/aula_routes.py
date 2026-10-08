from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.controllers.aula_controller import aula_controller

router = APIRouter(tags=["Aulas"])


class AulaEntrada(BaseModel):
    id_aluno: int = Field(examples=[5])
    id_professor: int = Field(examples=[2])
    data: str = Field(examples=["2026-10-20"], description="AAAA-MM-DD")
    hora: int = Field(examples=[15], description="Hora de início, de 7 a 21")
    duracao: int = Field(default=1, examples=[2], description="Em horas, de 1 a 3")


@router.post("/api/aulas", status_code=201)
def agendar_aula(dados: AulaEntrada):
    if not aula_controller.participantes_existem(dados.id_aluno, dados.id_professor):
        raise HTTPException(status_code=404, detail="Aluno ou professor não encontrado.")

    if aula_controller.horario_ocupado(
        dados.id_aluno, dados.id_professor, dados.data, dados.hora, dados.duracao
    ):
        raise HTTPException(
            status_code=409,
            detail="Aluno ou professor já tem aula nesse horário, ou atingiu o limite de aulas agendadas.",
        )

    try:
        return aula_controller.agendar(
            dados.id_aluno, dados.id_professor, dados.data, dados.hora, dados.duracao
        )
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro))


@router.post("/api/aulas/{id}/cancelar")
def cancelar_aula(id: int):
    try:
        aula = aula_controller.cancelar(id)
    except ValueError as erro:
        raise HTTPException(status_code=409, detail=str(erro))
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula não encontrada.")
    return aula


@router.get("/api/relatorio/faturamento", tags=["Relatórios"])
def faturamento():
    return aula_controller.faturamento()
