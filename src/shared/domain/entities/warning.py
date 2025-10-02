from pydantic import *
import uuid
from typing import *
import datetime

class Warning(BaseModel):
    
    warning_id: str = Field(
        description="ID do aviso",
        default_factory=lambda: str(uuid.uuid4())
    )
    title: str = Field(
        description="Título do aviso"
    )
    description: str = Field(
        description="Descrição do aviso"
    )
    expire: datetime.datetime = Field(
        description="Data de vencimento do aviso / data limite do aviso",
    )
    viewed: bool = Field(
        description="Bool para identificar se foi visualizado ou não"
    )
        
    model_config = ConfigDict(
        use_enum_values=False,
        extra="forbid"
    )