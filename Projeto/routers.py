from fastapi import APIRouter
from atleta.controller import router as atleta
from categoria.controller import router as categorias
from centro_treinamento.controller import router as centro_treino

api_router = APIRouter()
api_router.include_router(atleta, prefix='/atletas', tags=['atletas'])
api_router.include_router(categorias, prefix='/categorias', tags=['categorias'])
api_router.include_router(centro_treino, prefix='/centro_treino', tags=['centro_treino'])


