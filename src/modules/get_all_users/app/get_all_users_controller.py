from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest
from .get_all_users_usecase import GetAllUsersUsecase

class GetAllUsersController:
    def __init__(self, usecase: GetAllUsersUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('user_id') is None:
                raise MissingParameters('user_id')
            
            users = self.usecase(user_id=request.data.get('user_id'))

            viewmodel = GetAllUsersViewModel(users=users)

            return OK(body=viewmodel.to_dict())
        
        except MissingParameters as err:
            return BadRequest(body=err.message)
        
        except EntityError as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return BadRequest(body=err.args[0])