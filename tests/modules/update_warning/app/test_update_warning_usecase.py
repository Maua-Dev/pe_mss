import pytest
from src.modules.update_warning.app.update_warning_usecase import UpdateWarningUsecase
from src.shared.domain.entities.warning import Warning, WarningBody
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock


class Test_UpdateWarningUsecase:
    def test_update_warning_usecase_as_non_admin(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateWarningUsecase(repo=repo, user_repo=user_repo)

        new_warning: Warning = Warning(
            target_role=ROLE.USER,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title='Atualização de sistema',
                description='O sistema será atualizado no próximo fim de semana.',
                expire=1704067200000
            ),
            created_at=1672531200000
        )

        warning = usecase.repo.create_warning(new_warning)

        with pytest.raises(ForbiddenAction) as exc_info:
            usecase(
                warning_id=warning.warning_id,
                title='Atualização de sistema - versão 2',
                description='O sistema será atualizado no próximo fim de semana. Esta é a versão 2.',
                user_id='550e8400-e29b-41d4-a716-446655440002'  # Non-admin user
            )

        assert str(exc_info.value) == 'Only ADM users can update warnings.'

    def test_update_warning_usecase_as_admin(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateWarningUsecase(repo=repo, user_repo=user_repo)

        new_warning: Warning = Warning(
            target_role=ROLE.USER,
            target_org=ORGANIZATION.DEV,
            body=WarningBody(
                title='Atualização de sistema',
                description='O sistema será atualizado no próximo fim de semana.',
                expire=1704067200000
            ),
            created_at=1672531200000
        )

        warning = usecase.repo.create_warning(new_warning)

        updated_warning = usecase(
            warning_id=warning.warning_id,
            title='Atualização de sistema - versão 2',
            description='O sistema será atualizado no próximo fim de semana. Esta é a versão 2.',
            user_id='550e8400-e29b-41d4-a716-446655440001'  # Admin user
        )

        assert updated_warning.body.title == 'Atualização de sistema - versão 2'
        assert updated_warning.body.description == 'O sistema será atualizado no próximo fim de semana. Esta é a versão 2.'
        assert updated_warning.target_role == 'USER'
        assert updated_warning.target_org == 'DEV'

    def test_update_warning_usecase_with_nonexistent_warning_id(self):
        repo = WarningRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateWarningUsecase(repo=repo, user_repo=user_repo)

        with pytest.raises(Exception) as exc_info:
            usecase(
                warning_id='nonexistent-warning-id',
                title='Atualização de sistema - versão 2',
                description='O sistema será atualizado no próximo fim de semana. Esta é a versão 2.',
                user_id='550e8400-e29b-41d4-a716-446655440001'  # Admin user
            )

        assert str(exc_info.value) == 'No items found for nonexistent-warning-id'