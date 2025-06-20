from uuid import uuid4
from contrib.dependencias import DatabaseDependency
from fastapi import APIRouter, status, Body, HTTPException
from centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy.future import select
from pydantic import UUID4

router = APIRouter()

@router.post('/',summary='Criar um novo centro de treinamento',status_code=status.HTTP_201_CREATED,reponse_model=CentroTreinamentoOut)
async def post(db_session: DatabaseDependency, centro__treinamento_in: CentroTreinamentoIn = Body(...)) -> CentroTreinamentoOut:
    centro__treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro__treinamento_in.model_dump())
    centro_model = CentroTreinamentoModel(**centro__treinamento_out.model_dump())
    db_session.add(centro_model)
    await db_session.commit()
    return centro__treinamento_out


@router.get('/',summary='Consultar todos os centros de treinamento',status_code=status.HTTP_200_OK,reponse_model=list[CentroTreinamentoOut])
async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return centros

@router.get('/{id}',summary='Consultar uma centro de treinamento pelo id',status_code=status.HTTP_200_OK,reponse_model=CentroTreinamentoOut)
async def query( id: UUID4,db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    if not centro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro não encontrado no id: {id}')
    return centro