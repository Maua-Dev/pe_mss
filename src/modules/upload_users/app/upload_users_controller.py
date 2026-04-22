from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .upload_users_usecase import UploadUsersUsecase
from .upload_users_viewmodel import UploadUsersViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, Forbidden, NotFound, BadRequest, InternalServerError


class UploadUsersController:

    def __init__(self, usecase: UploadUsersUsecase):
        self.UploadUsersUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            requester_user = request.data.get('user_from_authorizer')
            
            if requester_user is None:
                raise MissingParameters('user_from_authorizer')
            
            requester_user_id = requester_user.get('id')

            file_base64 = request.data.get('file_base64')
            if file_base64 is None:
                raise MissingParameters('file_base64')

            if type(file_base64) is not str:
                raise WrongTypeParameter(
                    fieldName="file_base64",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(file_base64).__name__
                )

            created_users, duplicated_users = self.UploadUsersUsecase(file_base64=file_base64, requester_user_id=requester_user_id)

            print(f"Created: {len(created_users)} users. Duplicated: {len(duplicated_users)} users.")

            viewmodel = UploadUsersViewmodel(
                status=200,
                uploaded_users=created_users,
                duplicated_users=duplicated_users
            )

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:
            return NotFound(body={"message": err.message})

        except MissingParameters as err:
            return BadRequest(body={"message": err.message})

        except WrongTypeParameter as err:
            return BadRequest(body={"message": err.message})

        except EntityError as err:
            return BadRequest(body={"message": err.message})
        
        except ForbiddenAction as err:
            return Forbidden(body={"message": err.message})

        except Exception as err:
            return InternalServerError(body={"message": err.args[0]})
