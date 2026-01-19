from src.shared.clients.sm_client import SmClient
from .delete_warning_usecase import DeleteWarningUsecase
from .delete_warning_viewmodel import DeleteWarningViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Conflict, Forbidden, InternalServerError, NotFound

class DeleteWarningController:
    def __init__(self, usecase:DeleteWarningUsecase):
        self.delete_warning_usecase= usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            signature= request.data.get("signature")

            if signature:
                sm_client= SmClient()

                rule_name= request.data.get("rule_name")
                warning_id= request.data.get("warning_id")

                if not sm_client.verify(rule_name=rule_name, warning_id=warning_id, signature=signature):
                    return InternalServerError(body="Invalid signatur")
                

                deleted_warning= self.delete_warning_usecase(warning_id=warning_id)

            else:
                requester_user = request.data.get('user_from_authorizer')

                if requester_user is None:
                    raise MissingParameters('user_from_authorizer')
                
                requester_user_id = requester_user.get('id')
                
                warning_id= request.data.get('warning_id')

                if warning_id is None:
                    raise MissingParameters('warning_id')
            
                if type(warning_id) != str:
                    raise WrongTypeParameter(
                        fieldName="warning_id",
                        fieldTypeExpected="str",
                        fieldTypeReceived=warning_id.__class__.__name__
                    )
                
                deleted_warning= self.delete_warning_usecase(warning_id=warning_id, user_id=requester_user_id)

            return OK(body=DeleteWarningViewmodel(deleted_warning).to_dict())
        
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
            



        
        