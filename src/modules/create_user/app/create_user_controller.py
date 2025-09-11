import re
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.domain.entities.user import User
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.enums.active_enum import ACTIVE

class CreateUserController:
    def __init__(self, usecase: CreateUserUsecase):
        self.create_user_usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('user_from_authorizer') is None:
                raise MissingParameters('user_from_authorizer')

            if request.data['user_from_authorizer'].get('id') is None:
                raise MissingParameters('id')
            if request.data['user_from_authorizer'].get('displayName') is None:
                raise MissingParameters('displayName')
            if request.data['user_from_authorizer'].get('mail') is None:
                raise MissingParameters('mail')
            
            if type(request.data['user_from_authorizer'].get('id')) != str:
                raise WrongTypeParameter(
                    fieldName="id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data['user_from_authorizer'].get('id').__class__.__name__
                )
            
            if type(request.data['user_from_authorizer'].get('displayName')) != str:
                raise WrongTypeParameter(
                    fieldName="displayName",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data['user_from_authorizer'].get('displayName').__class__.__name__
                )
            
            if type(request.data['user_from_authorizer'].get('mail')) != str:
                raise WrongTypeParameter(
                    fieldName="mail",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data['user_from_authorizer'].get('mail').__class__.__name__
                )

            requested_user_role = self.create_user_usecase.repo.get_user(user_id=request.data['user_from_authorizer'].get('id')).role

            match requested_user_role:
                case ROLE.ADM:
                    # nome, email, organization; role
                    if request.data.get('name') is None:
                        raise MissingParameters('name')
                    
                    if request.data.get('email') is None:
                        raise MissingParameters('email')
                    
                    if request.data.get('organization') is None:
                        raise MissingParameters('organization')
                    
                    if request.data.get('role') is None:
                        raise MissingParameters('role')
                    
                    user=self.create_user_usecase(user_data=request.data, case=requested_user_role)

                case ROLE.PRESIDENT:
                    # nome*, email*, organization*, periodo, curso
                    if request.data.get('name') is None:
                        raise MissingParameters('name')
                    
                    if request.data.get('email') is None:
                        raise MissingParameters('email')
                    
                    if request.data.get('organization') is None:
                        raise MissingParameters('organization')
                    
                    if request.data.get('course') is None:
                        raise MissingParameters('course')
                    
                    if request.data.get('period') is None:
                        raise MissingParameters('period')
                    
                    user=self.create_user_usecase(user_data=request.data, case=requested_user_role)

                case _:
                    # Criando pela planilha
                    user=self.create_user_usecase(user_data=request.data, case="planilha")

            viewmodel= CreateUserViewmodel(user=user)

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