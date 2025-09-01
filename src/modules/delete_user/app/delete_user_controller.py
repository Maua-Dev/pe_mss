from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .delete_user_usecase import DeleteUserUsecase
from .delete_user_viewmodel import DeleteUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
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
            request_user_role = self.DeleteUserUsecase.repo.get_user(request_user_id).role
            
            if request_user_id != user_id:
                if request_user_role == ROLE.ADM:
                    user = self.DeleteUserUsecase(user_id=str(user_id))

                    viewmodel = DeleteUserViewmodel(user=user)
                    return OK(viewmodel.to_dict())

                elif request_user_role == ROLE.PRESIDENT and self.DeleteUserUsecase.repo.get_user(request_user_id).organization == self.DeleteUserUsecase.repo.get_user(user_id).organization:
                    user = self.DeleteUserUsecase(user_id=str(user_id))

                    viewmodel = DeleteUserViewmodel(user=user)
                    return OK(viewmodel.to_dict())


                raise Exception("Not enough permissions to complete the request")
            else:
                user = self.DeleteUserUsecase(user_id=str(user_id))

                viewmodel = DeleteUserViewmodel(user=user)
                return OK(viewmodel.to_dict())
        
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
