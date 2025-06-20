from datetime import datetime
from uuid import uuid4
from categoria.models import CategoriaModel
from contrib.dependencias import DatabaseDependency
from fastapi import APIRouter, status, Body, HTTPException
from atleta.schemas import AtletaIn, AtletaOut,AtletaUpdate
from atleta.models import AtletaModel
from sqlalchemy.future import select
from centro_treinamento.models import CentroTreinamentoModel
from pydantic import UUID4



router = APIRouter()

@router.post('/',summary='Criar um novo atleta',status_code=status.HTTP_201_CREATED,response_model=AtletaOut)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=AtletaIn.categoria.nome))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'A Categoria {AtletaIn.categoria.nome} não foi encontrada.')
 
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=AtletaIn.centro_treinamento.nome))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'O Centro de treinamento {AtletaIn.centro_treinamento.nome} não foi encontrado.')
    
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(),**atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria','centro_treinamento'}))
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        atleta_model.categoria_id = categoria.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Ocorrreu um erro ao inserir os dados no banco de dados.')

    return atleta_out
    

@router.get('/',summary='Consultar todas os atletas',status_code=status.HTTP_200_OK,reponse_model=list[AtletaOut])
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    return [AtletaOut.model_validate(atleta) for atleta in atletas]


@router.get('/{id}',summary='Consultar um atleta pelo id',status_code=status.HTTP_200_OK,reponse_model=AtletaOut)
async def query( id: UUID4,db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    return atleta


@router.patch('/{id}',summary='Editar um atleta pelo id',status_code=status.HTTP_200_OK,reponse_model=AtletaOut)
async def query( id: UUID4,db_session: DatabaseDependency,atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta,key,value)

    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta


@router.delete('/{id}',summary='Deletar um atleta pelo id',status_code=status.HTTP_204_NO_CONTENT,reponse_model=AtletaOut)
async def query( id: UUID4,db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    
    await db_session.delete(atleta)
    await db_session.commit()
