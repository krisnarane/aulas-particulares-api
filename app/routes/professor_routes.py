from fastapi import APIRouter, HTTPException

from app.controllers.professor_controller import professor_controller

router = APIRouter(prefix="/api/professores", tags=["Professores"])


@router.get("")
def listar_professores():
    return professor_controller.listar()


@router.get("/materia/{materia}")
def listar_por_materia(materia: str):
    return professor_controller.listar_por_materia(materia)


@router.get("/{id}")
def buscar_professor(id: int):
    professor = professor_controller.buscar(id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado.")
    return professor
