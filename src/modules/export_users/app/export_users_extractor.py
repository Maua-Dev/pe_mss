from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest


class DownloadUsersExtractor:
    def __init__(self, repo: IUserRepository):
        self.repo_user = repo
    
    def __call__(self, requester_user_id: str) -> dict:
        
        requester_user = self.repo_user.get_user(user_id=requester_user_id)
        
        if requester_user.role != ROLE.ADM:
            raise ForbiddenAction("You do not have permission to access this resource.")
        
        try:
            users= self.repo_user.get_all_user()

        except:
            raise NoItemsFound('memebers')
        
        users_dict= {}

        for user in users:
            users_dict[user.user_id]= {
                "name": user.name,
                "email": user.email,
                "ra": user.ra,
                "role": user.role.value,
                "state": user.state.value if user.state else None,
                "course": user.course.value if user.course else None,
                "year": user.year if user.year else None,
                "active": user.active.value if user.active else None,
                "organization": user.organization.value if user.organization else None
            }

        return users_dict
