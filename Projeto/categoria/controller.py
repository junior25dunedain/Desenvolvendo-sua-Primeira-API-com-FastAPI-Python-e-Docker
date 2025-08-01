from uuid import uuid4
from contrib.dependencias import DatabaseDependency
from fastapi import APIRouter, status, Body, HTTPException
from categoria.schemas import CategoriaIn, CategoriaOut
from categoria.models import CategoriaModel
from sqlalchemy.future import select
from pydantic import UUID4

router = APIRouter()

@router.post('/',summary='Criar uma nova categoria',status_code=status.HTTP_201_CREATED,reponse_model=CategoriaOut)
async def post(db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)) -> CategoriaOut:
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    db_session.add(categoria_model)
    await db_session.commit()
    return categoria_out


@router.get('/',summary='Consultar todas as Categorias',status_code=status.HTTP_200_OK,reponse_model=list[CategoriaOut])
async def query(db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return categorias

@router.get('/{id}',summary='Consultar uma Categoria pelo id',status_code=status.HTTP_200_OK,reponse_model=CategoriaOut)
async def query( id: UUID4,db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Categoria não encontrada no id: {id}')
    return categoria