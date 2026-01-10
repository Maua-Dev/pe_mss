from datetime import datetime
from src.modules.create_warning.app.create_warning_viewmodel import CreateWarningViewmodel
from src.shared.domain.entities.warning import Warning, WarningBody
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE


class Test_CreateWarningViewmodel:
    def test_create_warning_viewmodel_for_specif_org(self):
        warning = Warning(
            warning_id='e6112d17-c030-4d65-8b9f-e472d20055a5',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title="Test Warning Title",
                description="Test Warning Description",
                expire=datetime.now().replace(year=datetime.now().year + 1).isoformat()
            ),
            created_at=datetime(2025, 11, 28, 10, 0, 0)
        )

        warning_viewmodel = CreateWarningViewmodel(warning=warning)
        
        assert warning_viewmodel.warning == warning

    def test_create_warning_viewmodel_general_org(self):
        warning = Warning(
            warning_id='f7223e28-d141-5e76-9a0f-f573e31166b6',
            target_role=ROLE.USER,
            body=WarningBody(
                title="General Warning",
                description="This is a general warning",
                expire=datetime.now().replace(year=datetime.now().year + 1).isoformat()
            ),
            created_at=datetime(2025, 11, 28, 10, 0, 0)
        )

        warning_viewmodel = CreateWarningViewmodel(warning=warning)

        assert warning_viewmodel.warning == warning

    def test_create_warning_viewmodel_to_dict(self):
        warning = Warning(
            warning_id='a8334f39-e252-6f87-0b1g-g684f42277c7',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.NAWAT,
            body=WarningBody(
                title="NAWAT Warning",
                description="Important update for NAWAT",
                expire=datetime.now().replace(year=datetime.now().year + 1).isoformat()
            ),
            created_at=datetime(2025, 11, 28, 10, 0, 0)
        )

        warning_viewmodel = CreateWarningViewmodel(warning=warning)

        result = warning_viewmodel.to_dict()

        assert result == {
            "warning": {
                "warning_id": 'a8334f39-e252-6f87-0b1g-g684f42277c7',
                "target_role": ROLE.PRESIDENT.value,
                "target_org": ORGANIZATION.NAWAT.value,
                "body": {
                    "title": "NAWAT Warning",
                    "description": "Important update for NAWAT",
                    "expire": warning.body.expire,
                },
                "created_at": datetime(2025, 11, 28, 10, 0, 0),
            },
            "message": "the warning was created successfully"
        }

    def test_create_warning_viewmodel_to_dict_without_target_org(self):
        warning = Warning(
            warning_id='b9445g40-f363-7g98-1c2h-h795g53388d8',
            target_role=ROLE.ADM,
            body=WarningBody(
                title="Admin Alert",
                description="System maintenance scheduled",
                expire=datetime.now().replace(year=datetime.now().year + 1).isoformat()
            ),
            created_at=datetime(2025, 11, 28, 10, 0, 0)
        )

        warning_viewmodel = CreateWarningViewmodel(warning=warning)

        result = warning_viewmodel.to_dict()

        assert result["warning"]["warning_id"] == 'b9445g40-f363-7g98-1c2h-h795g53388d8'
        assert result["warning"]["target_role"] == ROLE.ADM.value
        assert result["warning"]["target_org"] is None
        assert result["warning"]["body"]["title"] == "Admin Alert"
        assert result["warning"]["body"]["description"] == "System maintenance scheduled"
        assert result["warning"]["body"]["expire"] == warning.body.expire
        assert result["warning"]["created_at"] == datetime(2025, 11, 28, 10, 0, 0)
        assert result["message"] == "the warning was created successfully"
