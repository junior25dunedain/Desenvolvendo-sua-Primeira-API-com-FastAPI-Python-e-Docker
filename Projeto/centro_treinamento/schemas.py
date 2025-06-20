from typing import Annotated

from pydantic import Field, UUID4
from contrib.schemas import BaseSchema

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento',example='CT king',max_length=20)]
    endereco: Annotated[str, Field(description='Endereço',example='rua fulano de tal',max_length=60)]
    proprietario: Annotated[str, Field(description='Nome do proprietario',example='jose rodriguez',max_length=30)]


class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento',example='CT king',max_length=20)]



class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]

