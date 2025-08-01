from categoria.schemas import CategoriaIn
from centro_treinamento.schemas import CentroTreinamentoAtleta
from pydantic import Field, PositiveFloat
from typing import Annotated, Optional
from contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta',example='Joao',max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta',example='12345678900',max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta',example=25)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta',example=75.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta',example=1.80)]
    sexo: Annotated[str, Field(description='Sexo do atleta',example='M',max_length=1)]
    categoria: Annotated[CategoriaIn,Field(description='categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta,Field(description='centro de treinamento do atleta')]


class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass


class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None,description='Nome do atleta',example='Joao',max_length=50)]
    idade: Annotated[Optional[int], Field(None,description='Idade do atleta',example=25)]
    sexo: Annotated[Optional[str], Field(None,description='Sexo do atleta',example='M',max_length=1)]
