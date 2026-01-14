
from .get_warning_usecase import GetWarningUsecase
from .get_warning_viewmodel import GetWarningViewModel
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Conflict, Forbidden, InternalServerError, NotFound


class GetWarningController:
    def __init__(self, usecase: GetWarningUsecase):
        self.get_warning_usecase = usecase
    
    def __call__(self, request: IRequest) -> IResponse:
        try:
            requester_user = request.data.get('user_from_authorizer')

            if requester_user is None:
                raise MissingParameters('user_from_authorizer')

            requester_user_id = requester_user.get('id')

            # I thought it could be usefull thinking on security. But for now I will not implement it.

            # requester_user_active= self.get_warning_usecase.get_user(user_id=requester_user_id).active

            # if requester_user_active.value != "ACTIVE":
            #     raise ForbiddenAction("Only Active users can ")

            warning_id= request.data.get('warning_id')

            role= request.data.get('role')

            organization= request.data.get('organization')

            if warning_id is None and role is None and organization is None:
                return BadRequest("You should inform warning_id or role and organization (at least one)")
            
            if warning_id:
                if role or organization:
                    return BadRequest("You should inform warning_id or role and organization (only one)")
                
                warning= self.get_warning_usecase(warning_id)
                
            if not role and organization or role and not organization:
                return BadRequest("You should inform role and organization")
            
            if role and organization:

                if not hasattr(ROLE, ROLE(role).name):
                    raise WrongTypeParameter(
                        fieldName="target_role",
                        fieldTypeExpected=f"one of {[role.name for role in ROLE]}",
                        fieldTypeReceived=role
                    )
                
                if not hasattr(ORGANIZATION, ORGANIZATION(organization).name):
                    raise WrongTypeParameter(
                        fieldName="organization",
                        fieldTypeExpected=f"one of {[org.name for org in ORGANIZATION]}",
                        fieldTypeReceived=organization
                    )
            
                warning= self.get_warning_usecase(role=ROLE(role), organization=ORGANIZATION(organization))

            viewmodel= GetWarningViewModel(warning=warning)

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)
        
        except DuplicatedItem as err:
            return Conflict(body=err.message)

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