import re
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound, Forbidden

class CreateUserController:
    def __init__(self, usecase: CreateUserUsecase):
        self.create_user_usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            
            #nao é necessario validar as entradas requester user pois isso o authorizer vai cuidar
            
            requester_user = request.data.get('user_from_authorizer')
            
            if requester_user:
                
                requester_user_id = request.data.get('user_from_authorizer').get('id')
                requester_user_role = self.create_user_usecase.repo.get_user(user_id=requester_user_id).role

            if request.data.get('new_user') is None:
                raise MissingParameters('new_user')
            
            if type(request.data.get('new_user')) == list:
                users = self.create_user_usecase(user_data=request.data, case="planilha", requester_id=requester_user_id)
                viewmodels = [CreateUserViewmodel(user=user).to_dict() for user in users]
                return OK(viewmodels)

            new_user_data = request.data.get('new_user')

            match requester_user_role:
                case ROLE.ADM:
                    # nome, email, organization; role
                    if new_user_data.get('name') is None:
                        raise MissingParameters('name')
                    
                    if new_user_data.get('email') is None:
                        raise MissingParameters('email')

                    if new_user_data.get('organization') is None:
                        raise MissingParameters('organization')

                    if new_user_data.get('role') is None:
                        raise MissingParameters('role')
                    
                    if not hasattr(ROLE, ROLE(new_user_data.get('role')).name):
                        raise WrongTypeParameter(
                            fieldName="role",
                            fieldTypeExpected=f"one of {[role.name for role in ROLE]}",
                            fieldTypeReceived=new_user_data.get('role')
                        )

                    if not hasattr(ORGANIZATION, ORGANIZATION(new_user_data.get('organization')).name):
                        raise WrongTypeParameter(
                            fieldName="organization",
                            fieldTypeExpected=f"one of {[org.name for org in ORGANIZATION]}",
                            fieldTypeReceived=new_user_data.get('organization')
                        )
                    
                    user=self.create_user_usecase(user_data=request.data, case=requester_user_role, requester_id=requester_user_id)
                case ROLE.PRESIDENT:
                    # nome*, email*, organization*, periodo, curso
                    if new_user_data.get('name') is None:
                        raise MissingParameters('name')
                    
                    if new_user_data.get('email') is None:
                        raise MissingParameters('email')

                    if new_user_data.get('organization') is None:
                        raise MissingParameters('organization')
                    
                    if not hasattr(ORGANIZATION, ORGANIZATION(new_user_data.get('organization')).name):
                        raise WrongTypeParameter(
                            fieldName="organization",
                            fieldTypeExpected=f"one of {[org.name for org in ORGANIZATION]}",
                            fieldTypeReceived=new_user_data.get('organization')
                        )

                    user=self.create_user_usecase(user_data=request.data, case=requester_user_role, requester_id=requester_user_id)

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
        
        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])