from datetime import datetime
from .create_warning_usecase import CreateWarningUsecase
from .create_warning_viewmodel import CreateWarningViewmodel
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Conflict, Forbidden, InternalServerError, NotFound


class CreateWarningController:
    def __init__(self, usecase:CreateWarningUsecase):
        self.create_warning_usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            requester_user = request.data.get('user_from_authorizer')

            if requester_user is None:
                raise MissingParameters('user_from_authorizer')

            requester_user_id = requester_user.get('id')
            
            new_warning_data = request.data.get('new_warning')

            if new_warning_data is None:
                raise MissingParameters('new_warning')
            
            if new_warning_data.get('title') is None:
                raise MissingParameters('title')
            
            if new_warning_data.get('description') is None:
                raise MissingParameters('description')
            
            if new_warning_data.get('expire') is None:
                raise MissingParameters('expire')
            
            expire_dt = datetime.fromisoformat(new_warning_data.get('expire'))
            
            if expire_dt <= datetime.now():
                raise WrongTypeParameter(
                    fieldName="expire",
                    fieldTypeExpected="a future date",
                    fieldTypeReceived=new_warning_data.get('expire')
                )
            
            if new_warning_data.get('target_role')is None:
                raise MissingParameters('target_role')
            
            if not hasattr(ROLE, ROLE(new_warning_data.get('target_role')).name):
                raise WrongTypeParameter(
                    fieldName="target_role",
                    fieldTypeExpected=f"one of {[role.name for role in ROLE]}",
                    fieldTypeReceived=new_warning_data.get('target_role')
                )
            
            if (new_warning_data.get('target_org') is None):
                # creates a new warning for all organizations

                new_general_warning = self.create_warning_usecase(
                    target_role=ROLE(new_warning_data.get('target_role')),
                    title=new_warning_data.get('title'),
                    description=new_warning_data.get('description'),
                    expire=expire_dt,
                    user_id=requester_user_id
                )

            else:
                # creates a new warning for a specific organization
                if not hasattr(ORGANIZATION, ORGANIZATION(new_warning_data.get('target_org')).name):
                    raise WrongTypeParameter(
                        fieldName="organization",
                        fieldTypeExpected=f"one of {[org.name for org in ORGANIZATION]}",
                        fieldTypeReceived=new_warning_data.get('target_org')
                    )

                new_specific_warning = self.create_warning_usecase(
                    target_role=ROLE(new_warning_data.get('target_role')),
                    target_org=ORGANIZATION(new_warning_data.get('target_org')),
                    title=new_warning_data.get('title'),
                    description=new_warning_data.get('description'),
                    expire=expire_dt,
                    user_id=requester_user_id
                )

            viewmodel= CreateWarningViewmodel(warning=new_specific_warning if new_warning_data.get('target_org') else new_general_warning)

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