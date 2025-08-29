# import pytest
# from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
# from src.shared.helpers.errors.domain_errors import EntityError
# from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


# class Test_DeleteUserUsecase:
#     def test_delete_user_usecase(self):
#         repo = UserRepositoryMock()
#         usecase = DeleteUserUsecase(repo=repo)
#         deleted_user = usecase(user_id=1)

#         assert deleted_user.user_id == 1
#         assert deleted_user.state.value == "deleted"

#     def test_delete_user_usecase_wrong_user_id(self):
#         repo = UserRepositoryMock()
#         usecase = DeleteUserUsecase(repo=repo)

#         with pytest.raises(EntityError):
#             usecase(user_id="1")

#     def test_delete_user_usecase_nonexistent_user_id(self):
#         repo = UserRepositoryMock()
#         usecase = DeleteUserUsecase(repo=repo)

#         with pytest.raises(EntityError):
#             usecase(user_id=3)

#     def test_delete_user_usecase_wrong_type_user_id(self):
#         repo = UserRepositoryMock()
#         usecase = DeleteUserUsecase(repo=repo)

#         with pytest.raises(EntityError):
#             usecase(user_id=1.5)