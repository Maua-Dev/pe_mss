from urllib3 import request
from src.modules.update_warning.app.update_warning_usecase import UpdateWarningUsecase
from src.modules.update_warning.app.update_warning_viewmodel import UpdateWarningViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Conflict, Forbidden, InternalServerError, NotFound


class UpdateWarningController:
    def __init__(self, usecase: UpdateWarningUsecase):
        self.usecase= usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            requester_user = request.data.get('user_from_authorizer')

            if requester_user is None:
                    raise MissingParameters('user_from_authorizer')

            requester_user_id = requester_user.get('id') if requester_user else None

            update_warning = request.data.get('update_warning')
            if update_warning is None:
                raise MissingParameters('update_warning')
            
            warning_id = update_warning.get('warning_id')
            if warning_id is None:
                raise MissingParameters('warning_id')
            
            updated_warning = update_warning.get('updated_warning')
            if updated_warning is None:
                raise MissingParameters('updated_warning')
            
            title = updated_warning.get('title')
            description = updated_warning.get('description')
            expire = updated_warning.get('expire')
            target_role = updated_warning.get('target_role')
            target_org = updated_warning.get('target_org')

            updated_warning = self.usecase(
                warning_id=warning_id,
                title=title,
                description=description,
                expire=expire,
                target_role=target_role,
                user_id=requester_user_id,
                target_org=target_org
            )

            viewmodel = UpdateWarningViewmodel(updated_warning)
            return OK(body=viewmodel.to_dict())
    
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