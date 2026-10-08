from fastapi import APIRouter, HTTPException

from app.controllers.aula_controller import aula_controller

router = APIRouter(prefix="/api/alunos", tags=["Alunos"])


@router.get("/{id}/aulas")
def aulas_do_aluno(id: int):
    aulas = aula_controller.aulas_do_aluno(id)
    if aulas is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    return aulas
