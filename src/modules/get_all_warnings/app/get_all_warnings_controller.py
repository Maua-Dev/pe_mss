from .get_all_warnings_usecase import GetAllWarningsUseCase
from .get_all_warnings_viewmodel import GetAllWarningsViewModel
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Conflict, Forbidden, InternalServerError, NotFound


class GetAllWarningsController:
    def __init__(self, usecase: GetAllWarningsUseCase):
        self.usecase = usecase

    def __call__(self,request: IRequest) -> IResponse:
        try:
            requester_user = request.data.get('user_from_authorizer')

            if requester_user is None:
                raise MissingParameters('user_from_authorizer')

            requester_user_id = requester_user.get('id')

            # requester_user_role = self.usecase.user_repo.get_user(user_id=requester_user_id).role

            # if requester_user_role != ROLE.ADM:
            #     raise ForbiddenAction("Only ADM users can get all warnings.")
            
            all_warnings = self.usecase(user_id=requester_user_id)

            viewmodel = GetAllWarningsViewModel(all_warnings)
            
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