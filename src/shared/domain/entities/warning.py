from pydantic import *
import uuid
from typing import *
from time import time

from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE

class WarningBody(BaseModel):
    title: str = Field(
        description="Título do aviso"
    )
    description: str = Field(
        description="Descrição do aviso"
    )
    expire: int = Field(
        description="Data de vencimento do aviso / data limite do aviso",
    )

class Warning(BaseModel):
    
    warning_id: str = Field(
        description="ID do aviso",
        default_factory=lambda: str(uuid.uuid4())
    )
    
    target_role: ROLE = Field(
        description="Role alvo do aviso",
        default=ROLE.PRESIDENT
    )
    
    target_org: ORGANIZATION = Field(
        description="Organização alvo do aviso",
        default=None
        # Turn to string in the model dump
    )
    
    body: WarningBody = Field(
        description="Corpo do aviso"
    )
    
    created_at: int= Field(
        description="Data de criação do aviso (timestamp em milisegundos)",
        default_factory=lambda: int(time() * 1000)
    )
        
    model_config = ConfigDict(
        use_enum_values=True,
        extra="forbid",
        populate_by_name=True
    )