import datetime

from src.modules.get_warning.app.get_warning_viewmodel import GetWarningViewModel, GetWarningViewModelInterface, WarningViewModel
from src.shared.domain.entities.warning import Warning, WarningBody
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE


class Test_GetWarningViewmodel:
    def test_warning_viewmodel(self):
        warning = Warning(
            warning_id='e6112d17-c030-4d65-8b9f-e472d20055a5',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title="Test Warning Title",
                description="Test Warning Description",
                expire=int(datetime.datetime(2025, 12, 31, 23, 59, 59, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 18, 10, 0, 0).timestamp() * 1000)
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
                expire=int(datetime.datetime(2025, 12, 15, 12, 0, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 18, 10, 0, 0).timestamp() * 1000)
        )

        warning_viewmodel = WarningViewModel(warning=warning)
        result = warning_viewmodel.to_dict()

        assert result["warning_id"] == 'f7223e28-d141-5e76-9a0f-f573e31166b6'
        assert result["target_role"] == ROLE.USER.value
        assert result["target_org"] == ORGANIZATION.NAWAT.value
        assert result["body"]["title"] == "General Warning"
        assert result["body"]["description"] == "This is a general warning"
        
    def test_warning_viewmodel_without_target_org(self):
        warning = Warning(
            warning_id='a8334f39-e252-6f87-0b1g-g684f42277c7',
            target_role=ROLE.ADM,
            body=WarningBody(
                title="Admin Warning",
                description="Important admin message",
                expire=int(datetime.datetime(2025, 12, 20, 18, 30, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 18, 10, 0, 0).timestamp() * 1000)
        )

        warning_viewmodel = WarningViewModel(warning=warning)
        result = warning_viewmodel.to_dict()

        assert result["warning_id"] == 'a8334f39-e252-6f87-0b1g-g684f42277c7'
        assert result["target_role"] == ROLE.ADM.value
        assert result["target_org"] is None
        
    def test_get_warning_viewmodel_interface(self):
        warning = Warning(
            warning_id='b9445g40-f363-7g98-1c2h-h795g53388d8',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.NAWAT,
            body=WarningBody(
                title="NAWAT Warning",
                description="Important update for NAWAT",
                expire=int(datetime.datetime(2025, 12, 20, 18, 30, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 18, 10, 0, 0).timestamp() * 1000)
        )

        get_warning_viewmodel = GetWarningViewModelInterface(warning=warning)

        assert get_warning_viewmodel.warning.warning_id == 'b9445g40-f363-7g98-1c2h-h795g53388d8'
        assert get_warning_viewmodel.warning.target_role == ROLE.PRESIDENT.value
        
    def test_get_warning_viewmodel_interface_to_dict(self):
        warning = Warning(
            warning_id='c0556h51-g474-8h09-2d3i-i806h64499e9',
            target_role=ROLE.USER,
            body=WarningBody(
                title="User Alert",
                description="Important user notification",
                expire=int(datetime.datetime(2025, 12, 25, 8, 0, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 18, 10, 0, 0).timestamp() * 1000)
        )

        get_warning_viewmodel = GetWarningViewModelInterface(warning=warning)
        result = get_warning_viewmodel.to_dict()

        assert result["warning"]["warning_id"] == 'c0556h51-g474-8h09-2d3i-i806h64499e9'
        assert result["warning"]["target_role"] == ROLE.USER.value
        assert result["warning"]["target_org"] is None
        assert result["warning"]["body"]["title"] == "User Alert"
        
    def test_get_warning_viewmodel_single_warning(self):
        warning = Warning(
            warning_id='e6112d17-c030-4d65-8b9f-e472d20055a5',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title="Warning 1",
                description="Description 1",
                expire=int(datetime.datetime(2025, 12, 31, 23, 59, 59, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 18, 10, 0, 0).timestamp() * 1000)
        )

        warnings_list = [warning]
        warning_viewmodel = GetWarningViewModel(warning=warnings_list)

        assert len(warning_viewmodel.warnings) == 1
        assert warning_viewmodel.warnings[0].warning.warning_id == 'e6112d17-c030-4d65-8b9f-e472d20055a5'
        
    def test_get_warning_viewmodel_multiple_warnings(self):
        warning1 = Warning(
            warning_id='e6112d17-c030-4d65-8b9f-e472d20055a5',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title="Warning 1",
                description="Description 1",
                expire=int(datetime.datetime(2025, 12, 31, 23, 59, 59, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 18, 10, 0, 0).timestamp() * 1000)
        )
        
        warning2 = Warning(
            warning_id='f7223e28-d141-5e76-9a0f-f573e31166b6',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.NAWAT,
            body=WarningBody(
                title="Warning 2",
                description="Description 2",
                expire=int(datetime.datetime(2025, 12, 15, 12, 0, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 18, 10, 0, 0).timestamp() * 1000)
        )

        warnings_list = [warning1, warning2]
        warning_viewmodel = GetWarningViewModel(warning=warnings_list)

        assert len(warning_viewmodel.warnings) == 2
        assert warning_viewmodel.warnings[0].warning.warning_id == 'e6112d17-c030-4d65-8b9f-e472d20055a5'
        assert warning_viewmodel.warnings[1].warning.warning_id == 'f7223e28-d141-5e76-9a0f-f573e31166b6'
        
    def test_get_warning_viewmodel_to_dict(self):
        warning1 = Warning(
            warning_id='e6112d17-c030-4d65-8b9f-e472d20055a5',
            target_role=ROLE.PRESIDENT,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title="Warning 1",
                description="Description 1",
                expire=int(datetime.datetime(2025, 12, 31, 23, 59, 59, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 18, 10, 0, 0).timestamp() * 1000)
        )
        
        warning2 = Warning(
            warning_id='f7223e28-d141-5e76-9a0f-f573e31166b6',
            target_role=ROLE.PRESIDENT,
            body=WarningBody(
                title="Warning 2",
                description="Description 2",
                expire=int(datetime.datetime(2025, 12, 15, 12, 0, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
            ),
            created_at=int(datetime.datetime(2025, 12, 18, 10, 0, 0).timestamp() * 1000)
        )

        warnings_list = [warning1, warning2]
        warning_viewmodel = GetWarningViewModel(warning=warnings_list)
        result = warning_viewmodel.to_dict()

        assert len(result["warnings"]) == 2
        assert result["warnings"][0]["warning"]["warning_id"] == 'e6112d17-c030-4d65-8b9f-e472d20055a5'
        assert result["warnings"][0]["warning"]["target_role"] == ROLE.PRESIDENT.value
        assert result["warnings"][0]["warning"]["target_org"] == ORGANIZATION.DEV.value
        assert result["warnings"][0]["warning"]["body"]["title"] == "Warning 1"
        
        assert result["warnings"][1]["warning"]["warning_id"] == 'f7223e28-d141-5e76-9a0f-f573e31166b6'
        assert result["warnings"][1]["warning"]["target_role"] == ROLE.PRESIDENT.value
        assert result["warnings"][1]["warning"]["target_org"] is None
        assert result["warnings"][1]["warning"]["body"]["title"] == "Warning 2"
        
        assert result["message"] == "The warning/s was/were retrieved successfully"
