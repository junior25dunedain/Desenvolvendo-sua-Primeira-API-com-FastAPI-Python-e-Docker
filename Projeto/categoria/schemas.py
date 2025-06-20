from contrib.schemas import BaseSchema 
from typing import Annotated
from pydantic import Field, UUID4


class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria',example='scale',max_length=10)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]
