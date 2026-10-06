# Professores cadastrados na plataforma.
# "perfil" diz qual classe vai ser criada (ver PERFIS em app/models/professor.py).
# Só o perfil "especialista" tem o campo "titulacao".

PROFESSORES = [
    {
        "id": 1,
        "perfil": "professor",
        "nome": "Ana Souza",
        "email": "ana.souza@email.com",
        "materia": "Matemática",
        "valor_hora": 80.0,
    },
    {
        "id": 2,
        "perfil": "especialista",
        "nome": "Carlos Mendes",
        "email": "carlos.mendes@email.com",
        "materia": "Matemática",
        "valor_hora": 120.0,
        "titulacao": "mestre",
    },
    {
        "id": 3,
        "perfil": "professor",
        "nome": "Beatriz Rocha",
        "email": "beatriz.rocha@email.com",
        "materia": "Inglês",
        "valor_hora": 70.0,
    },
    {
        "id": 4,
        "perfil": "professor",
        "nome": "Diego Martins",
        "email": "diego.martins@email.com",
        "materia": "Física",
        "valor_hora": 85.0,
    },
    {
        "id": 5,
        "perfil": "especialista",
        "nome": "Helena Costa",
        "email": "helena.costa@email.com",
        "materia": "Química",
        "valor_hora": 110.0,
        "titulacao": "doutor",
    },
    {
        "id": 6,
        "perfil": "professor",
        "nome": "Felipe Araújo",
        "email": "felipe.araujo@email.com",
        "materia": "Redação",
        "valor_hora": 75.0,
    },
]
