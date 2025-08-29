import re
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
            if request.data.get('id') is None:
                raise MissingParameters('id')
            if request.data.get('displayName') is None:
                raise MissingParameters('displayName')
            if request.data.get('mail') is None:
                raise MissingParameters('mail')
            
            if type(request.data.get('id')) != str:
                raise WrongTypeParameter(
                    fieldName="id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('id').__class__.__name__
                )
            
            if type(request.data.get('displayName')) != str:
                raise WrongTypeParameter(
                    fieldName="displayName",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('displayName').__class__.__name__
                )
            
            if type(request.data.get('mail')) != str:
                raise WrongTypeParameter(
                    fieldName="mail",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('mail').__class__.__name__
                )
                
            ra_pattern = r'[0-9]+\.[0-9]+-[0-9]+@maua\.br'
            has_ra = re.match(ra_pattern, request.data.get('mail'))
            
            if has_ra:
            
                new_user=User(
                    user_id= request.data.get('id'),
                    name= request.data.get('displayName'),
                    email= request.data.get('mail'),
                    state= STATE.PENDING,
                    role= ROLE.USER,
                    organization= None,
                    ra= request.data.get('mail').split('@')[0]
                )
                
            else:
                
                new_user=User(
                    user_id= request.data.get('id'),
                    name= request.data.get('displayName'),
                    email= request.data.get('mail'),
                    state= STATE.PENDING,
                    role= ROLE.USER,
                    organization= None,
                    ra= None
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