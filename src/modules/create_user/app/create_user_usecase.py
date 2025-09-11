import re
import uuid
from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.enums.role_enum import ROLE


class CreateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_data, case, requester_id) -> IUserRepository.create_user:
        match case:
            case ROLE.ADM:
                # nome, email, organization; role
                try:
                    user = User(
                        user_id=f"{uuid.uuid4()}",
                        name=user_data['new_user']['name'],
                        email=user_data['new_user']['email'],
                        role=ROLE(user_data['new_user']['role']),
                        organization=ORGANIZATION(user_data['new_user']['organization']),
                        active=ACTIVE.ACTIVE,
                        state=STATE.PENDING,
                        ra=re.search(r'(.+)@', user_data['new_user']['email']).group(1)
                    )

                    self.repo.has_permission_target_user(requester_id=requester_id, target_user=user)
                except Exception as e:
                    raise e
                
                new_user = self.repo.create_user(new_user=user)
                return new_user
            
            case ROLE.PRESIDENT:
                # nome*, email*, organization*, periodo, curso
                try:
                    user = User(
                        user_id=f"{uuid.uuid4()}",
                        name=user_data['new_user']['name'],
                        email=user_data['new_user']['email'],
                        role=ROLE.USER,
                        organization=ORGANIZATION(user_data['new_user']['organization']),
                        course=COURSE(user_data['new_user']['course']),
                        year=user_data['new_user']['year'],
                        active=ACTIVE.ACTIVE,
                        state=STATE.PENDING,
                        ra=re.search(r'(.+)@', user_data['new_user']['email']).group(1)
                    )

                    self.repo.has_permission_target_user(requester_id=requester_id, target_user=user)
                except Exception as e:
                    raise e
                
                new_user = self.repo.create_user(new_user=user)
                return new_user
            
            case "planilha": 
                created_users = []
                for new_user_data in user_data['new_user']:
                    try:
                        user = User(
                            user_id=f"{uuid.uuid4()}",
                            name=new_user_data['name'],
                            email=new_user_data['email'],
                            role=ROLE(new_user_data['role']),
                            organization=ORGANIZATION(new_user_data['organization']),
                            active=ACTIVE.ACTIVE,
                            state=STATE.PENDING,
                            ra=re.search(r'(.+)@', new_user_data['email']).group(1)
                        )

                        self.repo.has_permission_target_user(requester_id=requester_id, target_user=user)
                    except Exception as e:
                        raise e
                    
                    created_user = self.repo.create_user(new_user=user)
                    created_users.append(created_user)
                
                return created_users