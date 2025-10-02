from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .delete_user_usecase import DeleteUserUsecase
from .delete_user_viewmodel import DeleteUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class DeleteUserController:

    def __init__(self, usecase: DeleteUserUsecase):
        self.DeleteUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_id = request.data.get('user_id')

            if request.data.get('user_from_authorizer') is None:
                raise MissingParameters('user_from_authorizer')

            if user_id is None:
                raise MissingParameters('user_id')

            if type(user_id) != str:
                raise WrongTypeParameter(
                    fieldName="user_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=user_id.__class__.__name__
                )
            
            request_user_id = request.data['user_from_authorizer'].get('id')
            
            if self.DeleteUserUsecase.repo.has_permission_target_id(requester_id=request_user_id, target_id=user_id):
                user = self.DeleteUserUsecase(user_id)
                return OK(body=DeleteUserViewmodel(user).to_dict())

        except ForbiddenAction as err:

            return BadRequest(body=err.message)
        
        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except WrongTypeParameter as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])
