from src.modules.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.modules.auth_user.app.auth_user_viewmodel import AuthUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound


class AuthUserController:
    def __init__(self, usecase: AuthUserUsecase):
        self.AuthUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('user_id') is None:
                raise MissingParameters('user_id')
            if request.data.get('displayName') is None:
                raise MissingParameters('displayName')
            if request.data.get('email') is None:
                raise MissingParameters('email')
            
            if type(request.data.get('user_id')) != str:
                raise WrongTypeParameter(
                    fieldName="user_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('user_id').__class__.__name__
                )
            
            new_user=User(
                user_id= request.data.get('user_id'),
                name= request.data.get('displayName'),
                email= request.data.get('email'),
                state= STATE.PENDING,
                role= ROLE.USER,
                ra= request.data.get('email').split('@')[0]
            )

            user_and_number=self.AuthUserUsecase(user=new_user)

            viewmodel= AuthUserViewmodel(user=user_and_number[0], case_number=user_and_number[1])

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