from pydantic import *
import uuid
from typing import *

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
    viewed: bool = Field(
        description="Bool para identificar se foi visualizado ou não"
    )
    
    class Config:
        use_enum_values = False
        extra = "forbid"