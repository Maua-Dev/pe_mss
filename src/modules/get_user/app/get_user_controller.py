from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.modules.get_all_users.app.get_all_users_viewmodel import GetUserViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest


class GetUserController:

    def __init__(self, usecase: GetAllUsersUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('user_from_authorizer') is None:
                raise MissingParameters('user_from_authorizer')

            if request.data.get('user_from_authorizer').get('id') is None:
                raise MissingParameters('id')
            if request.data.get('user_from_authorizer').get('displayName') is None:
                raise MissingParameters('displayName')
            if request.data.get('user_from_authorizer').get('mail') is None:
                raise MissingParameters('mail')
            
            if type(request.data.get('user_from_authorizer').get('id')) != str:
                raise WrongTypeParameter(
                    fieldName="id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('user_from_authorizer').get('id').__class__.__name__
                )
            
            if type(request.data.get('user_from_authorizer').get('displayName')) != str:
                raise WrongTypeParameter(
                    fieldName="displayName",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('user_from_authorizer').get('displayName').__class__.__name__
                )
            
            if type(request.data.get('user_from_authorizer').get('mail')) != str:
                raise WrongTypeParameter(
                    fieldName="mail",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('user_from_authorizer').get('mail').__class__.__name__
                )

            requester_user_id = request.data.get('user_from_authorizer').get('id')
            user = self.usecase(user_id=requester_user_id)
            viewmodel = GetUserViewModel(user=user)

            return OK(viewmodel.to_dict())

        except MissingParameters as err:
            return BadRequest(body=err.message)
        
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        
        except NoItemsFound as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return BadRequest(body=err.args[0])