
import pytest
from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.external.postgres.datasources.postgres_datasource_tests import TestsRdsDatasource
from src.shared.infra.repositories.user_repository_postgres import UserRepositoryPostgres
import os


class TestUserRepositoryPostgres:
    IN_GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true'

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_get_all_user(self):
        datasource= TestsRdsDatasource()
        
        repo= UserRepositoryPostgres(db_datasource=datasource)

        response_all_users= repo.get_all_user()
        
        datasource.close()

        assert len(response_all_users) == 8

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_get_user(self):
        datasource= TestsRdsDatasource()

        repo = UserRepositoryPostgres(db_datasource=datasource)

        existing_user = User(
            user_id="b423780f-2045-44e1-9c0b-98352841817d",
            name="Murillo Strina",
            email="22.00730-0@maua.br",
            ra="22.00730-0",
            role=ROLE.USER,
            state=STATE.PENDING,
            active=ACTIVE.ACTIVE,
            course=COURSE.ECM,
            year=4,
            organization=ORGANIZATION.NAWAT
        )
    
        response_user = repo.get_user(user_id=existing_user.user_id)
        
        datasource.close()

        assert response_user == existing_user

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_has_permission_target_user(self):
        datasource= TestsRdsDatasource()

        repo= UserRepositoryPostgres(db_datasource=datasource)

        response= repo.has_permission_target_user(
            requester_id="550e8400-e29b-41d4-a716-446655440001",
            target_user=User(
                name="Heitor", 
                email="21.00453-7@maua.br", 
                ra="21.00453-7", 
                state=STATE.APPROVED, 
                role=ROLE.PRESIDENT, 
                active=ACTIVE.ACTIVE, 
                course=COURSE.ECM, 
                year=4, 
                organization=ORGANIZATION.NAWAT, user_id="550e8400-e29b-41d4-a716-446655440002"
            )
        )
        
        datasource.close()
        
        assert response == True

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_has_no_permission_if_target_user_is_a_president_tries_to_act_on_another_president(self):
        datasource= TestsRdsDatasource()

        repo= UserRepositoryPostgres(db_datasource=datasource)

        with pytest.raises(ForbiddenAction):
            repo.has_permission_target_user(
                requester_id="e6bed58f-424a-4b62-b408-18e0a8d1f069",
                target_user=User(
                    name="Heitor", 
                    email="21.00453-7@maua.br", 
                    ra="21.00453-7", 
                    state=STATE.APPROVED, 
                    role=ROLE.PRESIDENT, 
                    active=ACTIVE.ACTIVE, 
                    course=COURSE.ECM, 
                    year=4, 
                    organization=ORGANIZATION.NAWAT, user_id="550e8400-e29b-41d4-a716-446655440002"
                )                    
            )
        datasource.close()
            
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_has_permission_target_id(self):
        datasource= TestsRdsDatasource()

        repo= UserRepositoryPostgres(db_datasource=datasource)

        response= repo.has_permission_target_id(
            requester_id="550e8400-e29b-41d4-a716-446655440001",
            target_id="550e8400-e29b-41d4-a716-446655440002"
        )
        
        datasource.close()  
        
        assert response == True

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_has_no_permission_if_target_id_is_a_president_and_tries_to_act_on_another_president(self):
        datasource= TestsRdsDatasource()

        repo= UserRepositoryPostgres(db_datasource=datasource)

        with pytest.raises(ForbiddenAction):
            repo.has_permission_target_id(
                requester_id="e6bed58f-424a-4b62-b408-18e0a8d1f069",
                target_id="550e8400-e29b-41d4-a716-446655440002"
            )
            
        datasource.close()

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_update_user(self):
        datasource= TestsRdsDatasource()

        repo = UserRepositoryPostgres(db_datasource=datasource)

        updated_user= User(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            name="Guilherme",
            email="25.00178-5@maua.br",
            ra="25.00178-5",
            role=ROLE.PRESIDENT,
            state=STATE.APPROVED,
            active=ACTIVE.ACTIVE,
            course=COURSE.CIC,
            year=2,
            organization=ORGANIZATION.DEV
        )

        response_update_user= repo.update_user(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            new_active= ACTIVE.ACTIVE,
            new_state= STATE.APPROVED,
            new_role= ROLE.PRESIDENT,
            new_course= COURSE.CIC,
            new_year= 2,
            new_organization= ORGANIZATION.DEV
        )
        
        datasource.close()

        assert updated_user == response_update_user

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_update_user_only_some_fields(self):
        datasource= TestsRdsDatasource()

        repo = UserRepositoryPostgres(db_datasource=datasource)

        updated_user= User(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            name="Guilherme",
            email="25.00178-5@maua.br",
            ra="25.00178-5",
            role=ROLE.ADM,
            state=STATE.APPROVED,
            active=ACTIVE.ACTIVE,
        )

        response_update_user= repo.update_user(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            new_state= STATE.APPROVED,
            new_role= ROLE.ADM
        )
        
        datasource.close()

        assert updated_user == response_update_user

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_update_user_no_user_found(self):
        datasource= TestsRdsDatasource()

        repo = UserRepositoryPostgres(db_datasource=datasource)

        with pytest.raises(NoItemsFound):
            repo.update_user(
                user_id="non-existent-user-id",
                new_state= STATE.APPROVED,
                new_role= ROLE.ADM
            )
            
        datasource.close()
         
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")   
    def test_create_user(self):
        datasource= TestsRdsDatasource()

        repo = UserRepositoryPostgres(db_datasource=datasource)

        new_user = User(
            user_id="a1b2c3d4-e5f6-7890-1234-567890abcdef",
            name="Matue",
            email="24.00730-0@maua.br",
            ra="24.00730-0",
            role=ROLE.USER,
            state=STATE.PENDING,
            active=ACTIVE.ACTIVE,
            course=COURSE.ECM,
            year=4,
            organization=ORGANIZATION.NAWAT
        )

        response_user = repo.create_user(new_user)
        
        datasource.close()

        assert response_user == new_user
            
    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_delete_user(self):
        datasource= TestsRdsDatasource()

        repo = UserRepositoryPostgres(db_datasource=datasource)
        
        new_user = User(
            user_id="a1b2c3d4-e5f6-7890-1234-567890abcdef",
            name="Matue",
            email="24.00730-0@maua.br",
            ra="24.00730-0",
            role=ROLE.USER,
            state=STATE.PENDING,
            active=ACTIVE.ACTIVE,
            course=COURSE.ECM,
            year=4,
            organization=ORGANIZATION.NAWAT
        )

        user_id_to_delete = "a1b2c3d4-e5f6-7890-1234-567890abcdef"

        result = repo.delete_user(user_id=user_id_to_delete)
        
        datasource.close()

        assert new_user == result

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_get_users(self):
        datasource= TestsRdsDatasource()
        
        repo= UserRepositoryPostgres(db_datasource=datasource)

        response_all_users= repo.get_users()
        
        datasource.close()

        assert len(response_all_users) == 8

    @pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping tests in GitHub Actions environment")
    def test_get_users_approved_from_dev(self):
        datasource= TestsRdsDatasource()
        
        repo= UserRepositoryPostgres(db_datasource=datasource)

        response_all_users= repo.get_users(
            state=STATE.APPROVED,
            organization=ORGANIZATION.DEV
        )
        
        datasource.close()

        assert len(response_all_users) == 3