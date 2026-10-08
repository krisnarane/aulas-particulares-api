from fastapi import FastAPI

from app.routes import aluno_routes, aula_routes, professor_routes

app = FastAPI(
    title="Aulas Particulares API",
    description="Agendamento de aulas particulares entre alunos e professores.",
    version="1.0.0",
)

app.include_router(professor_routes.router)
app.include_router(aula_routes.router)
app.include_router(aluno_routes.router)
