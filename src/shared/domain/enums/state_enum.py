from enum import Enum


class STATE(Enum):
    APPROVED= "APPROVED"
    PENDING= "PENDING"
    REJECTED= "REJECTED"

class ROLE(Enum):
    ADM= "ADM"
    USER= "USER"
    PRESIDENT= "PRESIDENT"

class ENTITY(Enum):
    DEV= "DEV"
    ESPORTES= "ESPORTES"
    METAVERSO= "METAVERSO"
    GUARDIAN= "GUARDIAN"
    NAWAT= "NAWAT"




