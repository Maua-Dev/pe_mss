from src.shared.domain.entities.warning import Warning

class UpdateWarningViewmodel:
    def __init__(self, warning: Warning):
        self.warning = warning

    def to_dict(self):
        return {
            "updated_warning": {
                "warning_id": self.warning.warning_id,
                "target_role": self.warning.target_role,
                "target_org": self.warning.target_org if self.warning.target_org else None,
                "body": {
                    "title": self.warning.body.title,
                    "description": self.warning.body.description,
                    "expire": self.warning.body.expire,
                },
                "created_at": self.warning.created_at,
            },
            "message": "the warning was created successfully"
        }