from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .update_user_usecase import UpdateUserUsecase
from .update_user_viewmodel import UpdateUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION


class UpdateUserController:
    def __init__(self, usecase: UpdateUserUsecase):
        self.usecase = usecase  

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('user_id') is None or request.data.get('user_id') == "":
                raise MissingParameters('user_id')

            new_state = request.data.get("new_state")
            new_role = request.data.get("new_role")
            new_course = request.data.get("new_course")
            new_year = request.data.get("new_year")
            new_organization = request.data.get("new_organization")
            new_active = request.data.get("new_active")

            if new_state is not None and not isinstance(new_state, str):
                raise WrongTypeParameter("new_state", "STATE", type(new_state).__name__)
            
            if new_role is not None and not isinstance(new_role, str):
                raise WrongTypeParameter("new_role", "ROLE", type(new_role).__name__)
            
            if new_course is not None and not isinstance(new_course, str):  
                raise WrongTypeParameter("new_course", "COURSE", type(new_course).__name__)
            
            if new_year is not None and not isinstance(new_year, int):
                raise WrongTypeParameter("new_year", "int", type(new_year).__name__)
            
            if new_organization is not None and not isinstance(new_organization, str):
                raise WrongTypeParameter("new_organization", "ORGANIZATION", type(new_organization).__name__)
            
            if new_active is not None and not isinstance(new_active, str):
                raise WrongTypeParameter("new_active", "bool", type(new_active).__name__)

            user = self.usecase(
                user_id=request.data.get("user_id"),
                new_state=new_state,
                new_role=new_role,
                new_course=new_course,
                new_year=new_year,
                new_organization=new_organization,
                new_active=new_active
            )

            viewmodel = UpdateUserViewmodel(user)
            return OK(viewmodel.to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)
        except (MissingParameters, WrongTypeParameter, EntityError) as err:
            return BadRequest(body=err.message)
        except Exception as err:
            return InternalServerError(body=str(err))
