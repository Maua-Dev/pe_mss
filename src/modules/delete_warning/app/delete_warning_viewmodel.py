class DeleteWarningViewmodel:
    def __init__(self, warning):
        self.warning= warning

    def to_dict(self):
        return {
            "warning": {
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
            "message": "the warning was deleted successfully"
        }