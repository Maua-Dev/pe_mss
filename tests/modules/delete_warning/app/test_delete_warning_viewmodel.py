import datetime

from src.modules.delete_warning.app.delete_warning_viewmodel import DeleteWarningViewmodel
from src.shared.domain.entities.warning import Warning, WarningBody
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE


class Test_DeleteWarningViewmodel:
    def test_delete_warning_viewmodel(self):
        warning = Warning(
            warning_id='e6112d17-c030-4d65-8b9f-e472d20055a5',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title="Test Warning Title",
                description="Test Warning Description",
                expire=int(datetime.datetime(2025, 12, 31, 23, 59, 59, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 10, 10, 0, 0).timestamp() * 1000)
        )

        warning_viewmodel = DeleteWarningViewmodel(warning=warning)
        
        assert warning_viewmodel.warning == warning

    def test_delete_warning_viewmodel_general(self):
        warning = Warning(
            warning_id='f7223e28-d141-5e76-9a0f-f573e31166b6',
            target_role=ROLE.USER,
            body=WarningBody(
                title="General Warning",
                description="This is a general warning",
                expire=int(datetime.datetime(2025, 12, 15, 12, 0, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 10, 10, 0, 0).timestamp() * 1000)
        )

        warning_viewmodel = DeleteWarningViewmodel(warning=warning)

        assert warning_viewmodel.warning == warning

    def test_delete_warning_viewmodel_to_dict(self):
        warning = Warning(
            warning_id='a8334f39-e252-6f87-0b1g-g684f42277c7',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.NAWAT,
            body=WarningBody(
                title="NAWAT Warning",
                description="Important update for NAWAT",
                expire=int(datetime.datetime(2025, 12, 20, 18, 30, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 10, 10, 0, 0).timestamp() * 1000)
        )

        warning_viewmodel = DeleteWarningViewmodel(warning=warning)

        result = warning_viewmodel.to_dict()

        assert result == {
            "warning": {
                "warning_id": 'a8334f39-e252-6f87-0b1g-g684f42277c7',
                "target_role": ROLE.PRESIDENT.value,
                "target_org": ORGANIZATION.NAWAT.value,
                "body": {
                    "title": "NAWAT Warning",
                    "description": "Important update for NAWAT",
                    "expire": int(datetime.datetime(2025, 12, 20, 18, 30, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000),
                },
                "created_at": int(datetime.datetime(2025, 12, 10, 10, 0, 0).timestamp() * 1000),
            },
            "message": "the warning was deleted successfully"
        }

    def test_delete_warning_viewmodel_to_dict_without_target_org(self):
        warning = Warning(
            warning_id='b9445g40-f363-7g98-1c2h-h795g53388d8',
            target_role=ROLE.ADM,
            body=WarningBody(
                title="Admin Alert",
                description="System maintenance scheduled",
                expire=int(datetime.datetime(2025, 12, 10, 8, 0, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 10, 10, 0, 0).timestamp() * 1000)
        )

        warning_viewmodel = DeleteWarningViewmodel(warning=warning)

        result = warning_viewmodel.to_dict()

        assert result["warning"]["warning_id"] == 'b9445g40-f363-7g98-1c2h-h795g53388d8'
        assert result["warning"]["target_role"] == ROLE.ADM.value
        assert result["warning"]["target_org"] is None
        assert result["warning"]["body"]["title"] == "Admin Alert"
        assert result["warning"]["body"]["description"] == "System maintenance scheduled"
        assert result["warning"]["body"]["expire"] == int(datetime.datetime(2025, 12, 10, 8, 0, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
        assert result["warning"]["created_at"] == int(datetime.datetime(2025, 12, 10, 10, 0, 0).timestamp() * 1000)
        assert result["message"] == "the warning was deleted successfully"
