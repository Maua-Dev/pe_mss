from typing import List
from src.shared.domain.entities.warning import Warning

class WarningViewModel:
    warning_id: str
    target_role: str
    target_org: str | None
    body: dict
    created_at: str
    title: str
    description: str
    expire: int
    created_at: str

    def __init__(self, warning: Warning):
        self.warning_id = warning.warning_id
        self.target_role = warning.target_role
        self.target_org = warning.target_org if warning.target_org else None
        self.body = {
            "title": warning.body.title,
            "description": warning.body.description,
            "expire": warning.body.expire,
        }
        self.created_at = warning.created_at


    def to_dict(self):
        return {
            "warning_id": self.warning_id,
            "target_role": self.target_role,
            "target_org": self.target_org,
            "body": self.body,
            "created_at": self.created_at,
        }
    
class GetWarningViewModel:
    warning: WarningViewModel

    def __init__(self, warning: Warning):
        self.warning = WarningViewModel(warning)

    def to_dict(self):
        return {
            "warning": self.warning.to_dict()
        }

class GetAllWarningsViewModel:
    warnings: List[GetWarningViewModel]

    def __init__(self, warnings: List[Warning]):
        self.warnings = []

        for warning in warnings:
            self.warnings.append(GetWarningViewModel(warning))

    def to_dict(self):
        return {
            "warnings": [warning.to_dict() for warning in self.warnings],
            "message": "The warnings were retrieved successfully"
        }