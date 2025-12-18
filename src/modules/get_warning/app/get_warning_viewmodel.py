from typing import List


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
    
class GetWarningViewModelInterface:
    warning: WarningViewModel

    def __init__(self, warning: Warning):
        self.warning = WarningViewModel(warning)

    def to_dict(self):
        return {
            "warning": self.warning.to_dict()
        }

class GetWarningViewModel:
    warnings: List[GetWarningViewModelInterface]

    def __init__(self, warning: List[Warning]):
        self.warnings = []

        for warning in warning:
            self.warnings.append(GetWarningViewModelInterface(warning))

    def to_dict(self):
        return {
            "warnings": [warning.to_dict() for warning in self.warnings],
            "message": "The warning/s was/were retrieved successfully"
        }