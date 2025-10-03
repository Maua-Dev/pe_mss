from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from .update_user_usecase import UpdateUserUsecase
from .update_user_viewmodel import UpdateUserViewmodel
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.state_enum import STATE


class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            
            if request.data.get('user_id') is None:
                raise MissingParameters('user_id')

            if type(request.data.get("name")) != str:
                raise WrongTypeParameter("name", "str", type(request.data.get("name")).__name__)
            if type(request.data.get("email")) != str:
                raise WrongTypeParameter("email", "str", type(request.data.get("email")).__name__)
            if type(request.data.get("ra")) != str:
                raise WrongTypeParameter("ra", "str", type(request.data.get("ra")).__name__)
            if type(request.data.get("user_id")) != str:
                raise WrongTypeParameter("user_id", "str", type(request.data.get("user_id")).__name__)

            
            try:
                state = STATE[request.data.get("new_state")]
            except KeyError:
                raise EntityError("new_state")

            try:
                role = ROLE[request.data.get("new_role")]
            except KeyError:
                raise EntityError("new_role")

            
            course = None
            if request.data.get("new_course") is not None:
                try:
                    course = COURSE[request.data.get("new_course")]
                except KeyError:
                    raise EntityError("new_course")

            year = request.data.get("new_year")
            if year is not None and type(year) != int:
                raise WrongTypeParameter("new_year", "int", type(year).__name__)

            organization = None
            if request.data.get("new_organization") is not None:
                try:
                    organization = ORGANIZATION[request.data.get("new_organization")]
                except KeyError:
                    raise EntityError("new_organization")

            
            user = self.usecase(
                name=request.data.get("name"),
                email=request.data.get("email"),
                ra=request.data.get("ra"),
                new_state=state,
                new_role=role,
                new_course=course,
                new_year=year,
                new_organization=organization,
                user_id=request.data.get("user_id"),
            )


            
            viewmodel = UpdateUserViewmodel(user)
            return OK(viewmodel.to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except (MissingParameters, WrongTypeParameter, EntityError) as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))
