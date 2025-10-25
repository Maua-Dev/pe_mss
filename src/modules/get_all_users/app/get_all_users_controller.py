from .get_all_users_viewmodel import GetAllUsersViewModel
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
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
            if request.data.get('user_from_authorizer') is None:
                raise MissingParameters('user_from_authorizer')

            requester_user_id = request.data.get('user_from_authorizer').get('id')
            name = request.data.get('name', None) if request.data.get('name', None) != "" else None
            ra = request.data.get('ra', None) if request.data.get('ra', None) != "" else None
            state = request.data.get('state', None) if request.data.get('state', None) != "" else None
            role = request.data.get('role', None) if request.data.get('role', None) != "" else None
            active = request.data.get('active', None) if request.data.get('active', None) != "" else None
            course = request.data.get('course', None) if request.data.get('course', None) != "" else None
            year = request.data.get('year', None) if request.data.get('year', None) != "" else None
            organization = request.data.get('organization', None) if request.data.get('organization', None) != "" else None
            
            if name and not isinstance(name, str):
                raise WrongTypeParameter("name", "str", type(name).__name__)
            if ra and not isinstance(ra, str):
                raise WrongTypeParameter("ra", "str", type(ra).__name__)
            if state and not isinstance(state, str):
                raise WrongTypeParameter("state", "str", type(state).__name__)
            if role and not isinstance(role, str):
                raise WrongTypeParameter("role", "str", type(role).__name__)
            if active and not isinstance(active, str):
                raise WrongTypeParameter("active", "str", type(active).__name__)
            if course and not isinstance(course, str):
                raise WrongTypeParameter("course", "str", type(course).__name__)
            
            if year is not None:
                if year.find('.') != -1:
                    raise WrongTypeParameter("year", "int", "float")
                try:
                    year = int(year)
                except (ValueError, TypeError):
                    raise WrongTypeParameter("year", "int", type(year).__name__)

            if organization and not isinstance(organization, str):
                raise WrongTypeParameter("organization", "str", type(organization).__name__)

            users, requester_role = self.usecase(user_id=requester_user_id, name=name, ra=ra, state=state, role=role, active=active, course=course, year=year, organization=organization)
            viewmodel = GetAllUsersViewModel(users=users, requester_role=requester_role, requester_id=requester_user_id).to_dict()
            
            return OK(viewmodel)
        
        except MissingParameters as err:
            return BadRequest(body=err.message)
        
        except EntityError as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return BadRequest(body=err.args[0])