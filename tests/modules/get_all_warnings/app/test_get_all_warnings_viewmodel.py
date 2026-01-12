import datetime

from src.modules.get_all_warnings.app.get_all_warnings_viewmodel import GetAllWarningsViewModel, GetWarningViewModel, WarningViewModel
from src.shared.domain.entities.warning import Warning, WarningBody
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE


class Test_GetAllWarningsViewmodel:
    def test_warning_viewmodel(self):
        warning = Warning(
            warning_id='e6112d17-c030-4d65-8b9f-e472d20055a5',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title="Test Warning Title",
                description="Test Warning Description",
                expire=datetime.datetime(2025, 12, 31, 23, 59, 59)
            ),
            created_at=datetime.datetime(2025, 12, 17, 10, 0, 0)
        )

        warning_viewmodel = WarningViewModel(warning=warning)
        
        assert warning_viewmodel.warning_id == 'e6112d17-c030-4d65-8b9f-e472d20055a5'
        assert warning_viewmodel.target_role == ROLE.PRESIDENT.value
        assert warning_viewmodel.target_org == ORGANIZATION.DEV.value
        assert warning_viewmodel.body["title"] == "Test Warning Title"
        assert warning_viewmodel.body["description"] == "Test Warning Description"
        
    def test_warning_viewmodel_to_dict(self):
        warning = Warning(
            warning_id='f7223e28-d141-5e76-9a0f-f573e31166b6',
            target_role=ROLE.USER,
            target_org=ORGANIZATION.NAWAT,
            body=WarningBody(
                title="General Warning",
                description="This is a general warning",
                expire=datetime.datetime(2025, 12, 15, 12, 0, 0)
            ),
            created_at=datetime.datetime(2025, 12, 17, 10, 0, 0)
        )

        warning_viewmodel = WarningViewModel(warning=warning)
        result = warning_viewmodel.to_dict()

        assert result["warning_id"] == 'f7223e28-d141-5e76-9a0f-f573e31166b6'
        assert result["target_role"] == ROLE.USER.value
        assert result["target_org"] == ORGANIZATION.NAWAT.value
        assert result["body"]["title"] == "General Warning"
        assert result["body"]["description"] == "This is a general warning"
        
    def test_get_warning_viewmodel(self):
        warning = Warning(
            warning_id='a8334f39-e252-6f87-0b1g-g684f42277c7',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.NAWAT,
            body=WarningBody(
                title="NAWAT Warning",
                description="Important update for NAWAT",
                expire=datetime.datetime(2025, 12, 20, 18, 30, 0)
            ),
            created_at=datetime.datetime(2025, 12, 17, 10, 0, 0)
        )

        get_warning_viewmodel = GetWarningViewModel(warning=warning)

        assert get_warning_viewmodel.warning.warning_id == 'a8334f39-e252-6f87-0b1g-g684f42277c7'
        assert get_warning_viewmodel.warning.target_role == ROLE.PRESIDENT.value
        
    def test_get_warning_viewmodel_to_dict(self):
        warning = Warning(
            warning_id='b9445g40-f363-7g98-1c2h-h795g53388d8',
            target_role=ROLE.ADM,
            body=WarningBody(
                title="Admin Alert",
                description="System maintenance scheduled",
                expire=datetime.datetime(2025, 12, 10, 8, 0, 0)
            ),
            created_at=datetime.datetime(2025, 12, 17, 10, 0, 0)
        )

        get_warning_viewmodel = GetWarningViewModel(warning=warning)
        result = get_warning_viewmodel.to_dict()

        assert result["warning"]["warning_id"] == 'b9445g40-f363-7g98-1c2h-h795g53388d8'
        assert result["warning"]["target_role"] == ROLE.ADM.value
        assert result["warning"]["target_org"] is None
        assert result["warning"]["body"]["title"] == "Admin Alert"
        
    def test_get_all_warnings_viewmodel(self):
        warning1 = Warning(
            warning_id='e6112d17-c030-4d65-8b9f-e472d20055a5',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title="Warning 1",
                description="Description 1",
                expire=datetime.datetime(2025, 12, 31, 23, 59, 59)
            ),
            created_at=datetime.datetime(2025, 12, 17, 10, 0, 0)
        )
        
        warning2 = Warning(
            warning_id='f7223e28-d141-5e76-9a0f-f573e31166b6',
            target_role=ROLE.USER,
            target_org=ORGANIZATION.NAWAT,
            body=WarningBody(
                title="Warning 2",
                description="Description 2",
                expire=datetime.datetime(2025, 12, 15, 12, 0, 0)
            ),
            created_at=datetime.datetime(2025, 12, 17, 10, 0, 0)
        )

        warnings_list = [warning1, warning2]
        all_warnings_viewmodel = GetAllWarningsViewModel(warnings=warnings_list)

        assert len(all_warnings_viewmodel.warnings) == 2
        assert all_warnings_viewmodel.warnings[0].warning.warning_id == 'e6112d17-c030-4d65-8b9f-e472d20055a5'
        assert all_warnings_viewmodel.warnings[1].warning.warning_id == 'f7223e28-d141-5e76-9a0f-f573e31166b6'
        
    def test_get_all_warnings_viewmodel_to_dict(self):
        warning1 = Warning(
            warning_id='e6112d17-c030-4d65-8b9f-e472d20055a5',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title="Warning 1",
                description="Description 1",
                expire=datetime.datetime(2025, 12, 31, 23, 59, 59)
            ),
            created_at=datetime.datetime(2025, 12, 17, 10, 0, 0)
        )
        
        warning2 = Warning(
            warning_id='f7223e28-d141-5e76-9a0f-f573e31166b6',
            target_role=ROLE.USER,
            body=WarningBody(
                title="Warning 2",
                description="Description 2",
                expire=datetime.datetime(2025, 12, 15, 12, 0, 0)
            ),
            created_at=datetime.datetime(2025, 12, 17, 10, 0, 0)
        )

        warnings_list = [warning1, warning2]
        all_warnings_viewmodel = GetAllWarningsViewModel(warnings=warnings_list)
        result = all_warnings_viewmodel.to_dict()

        assert len(result["warnings"]) == 2
        assert result["warnings"][0]["warning"]["warning_id"] == 'e6112d17-c030-4d65-8b9f-e472d20055a5'
        assert result["warnings"][0]["warning"]["target_role"] == ROLE.PRESIDENT.value
        assert result["warnings"][0]["warning"]["target_org"] == ORGANIZATION.DEV.value
        assert result["warnings"][0]["warning"]["body"]["title"] == "Warning 1"
        
        assert result["warnings"][1]["warning"]["warning_id"] == 'f7223e28-d141-5e76-9a0f-f573e31166b6'
        assert result["warnings"][1]["warning"]["target_role"] == ROLE.USER.value
        assert result["warnings"][1]["warning"]["target_org"] is None
        assert result["warnings"][1]["warning"]["body"]["title"] == "Warning 2"
        
        assert result["message"] == "The warnings were retrieved successfully"
