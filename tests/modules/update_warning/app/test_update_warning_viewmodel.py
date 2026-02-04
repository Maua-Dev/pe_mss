from datetime import datetime
from src.modules.update_warning.app.update_warning_viewmodel import UpdateWarningViewmodel
from src.shared.domain.entities.warning import Warning, WarningBody
from src.shared.domain.enums.role_enum import ROLE


class Test_UpdateWarningViewmodel:
    def test_update_warning_viewmodel_general(self):
        warning = Warning(
            warning_id="e6112d17-c030-4d65-8b9f-e472d20055a5",
            target_role=ROLE.USER,
            body=WarningBody(
                title="General Warning",
                description="This is a general warning for all organizations",
                expire=int(datetime.now().replace(year=datetime.now().year + 1).timestamp() * 1000)
            ),
            created_at=int(datetime(2025, 11, 28, 10, 0, 0).timestamp() * 1000)
        )

        warning_viewmodel = UpdateWarningViewmodel(warning=warning)

        assert warning_viewmodel.warning == warning

    def test_update_warning_viewmodel_to_dict(self):
        warning = Warning(
            warning_id="f7223e28-d141-5e76-9a0f-f573e31166b6",
            target_role=ROLE.PRESIDENT,
            target_org="NAWAT",
            body=WarningBody(
                title="NAWAT Warning",
                description="Important update for NAWAT organization",
                expire=int(datetime.now().replace(year=datetime.now().year + 1).timestamp() * 1000)
            ),
            created_at=int(datetime(2025, 11, 28, 10, 0, 0).timestamp() * 1000)
        )

        warning_viewmodel = UpdateWarningViewmodel(warning=warning)

        result = warning_viewmodel.to_dict()

        assert result == {
            "updated_warning": {
                "warning_id": "f7223e28-d141-5e76-9a0f-f573e31166b6",
                "target_role": "PRESIDENT",
                "target_org": "NAWAT",
                "body": {
                    "title": "NAWAT Warning",
                    "description": "Important update for NAWAT organization",
                    "expire": warning.body.expire
                },
                "created_at": warning.created_at
            },
            "message": "the warning was updated successfully"
        }

    def test_update_warning_viewmodel_to_dict_no_target_org(self):
        warning = Warning(
            warning_id="a8334f39-e252-6f87-0b1g-g684f42277c7",
            target_role=ROLE.USER,
            body=WarningBody(
                title="System Update",
                description="The system will be updated this weekend.",
                expire=int(datetime.now().replace(year=datetime.now().year + 1).timestamp() * 1000)
            ),
            created_at=int(datetime(2025, 11, 28, 10, 0, 0).timestamp() * 1000)
        )

        warning_viewmodel = UpdateWarningViewmodel(warning=warning)

        result = warning_viewmodel.to_dict()

        assert result == {
            "updated_warning": {
                "warning_id": "a8334f39-e252-6f87-0b1g-g684f42277c7",
                "target_role": "USER",
                "target_org": None,
                "body": {
                    "title": "System Update",
                    "description": "The system will be updated this weekend.",
                    "expire": warning.body.expire
                },
                "created_at": warning.created_at
            },
            "message": "the warning was updated successfully"
        }