from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class DownloadUsersExtractor:
    def __init__(self, repo: IUserRepository):
        self.repo_user = repo

    def __call__(self):
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
                "state": user.state if hasattr(user.state, 'state') else user.state.value,
                "course": user.course.value if hasattr(user.course, 'course') else user.course.value,
                "year": user.year if hasattr(user.year, 'year') else user.year,
                "active": user.active if hasattr(user.active, 'active') else user.active.value,
                "organization": user.organization if hasattr(user.organization, 'organization') else user.organization.value
            }

        return users_dict
