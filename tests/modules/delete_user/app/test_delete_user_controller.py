# from src.modules.delete_user.app.delete_user_controller import DeleteUserController
# from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
# from src.shared.helpers.external_interfaces.http_models import HttpRequest
# from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


# class Test_DeleteUserController:
#     def test_delete_user_controller(self):
#         repo = UserRepositoryMock()
#         usecase = DeleteUserUsecase(repo=repo)
#         controller = DeleteUserController(usecase=usecase)

#         request = HttpRequest(body={
#             'user_id': "1"
#         })

#         response = controller(request=request)

#         assert response.status_code == 200
#         assert response.body['user_id'] == repo.users[0].user_id
#         assert response.body['message'] == "the user was deleted successfully"

#     def test_delete_user_controller_missing_user_id(self):
#         repo = UserRepositoryMock()
#         usecase = DeleteUserUsecase(repo=repo)
#         controller = DeleteUserController(usecase=usecase)

#         request = HttpRequest(body={
#         })

#         response = controller(request=request)

#         assert response.status_code == 400
#         assert response.body == "Field user_id is missing"

#     def test_delete_user_controller_invalid_user_id(self):
#         repo = UserRepositoryMock()
#         usecase = DeleteUserUsecase(repo=repo)
#         controller = DeleteUserController(usecase=usecase)

#         request = HttpRequest(body={
#             'user_id': 3
#         })

#         response = controller(request=request)

#         assert response.status_code == 400
#         assert response.body == "Field user_id is expecting str type, but received int type"