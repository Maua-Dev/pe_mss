import re
import uuid
from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.course_enum import COURSE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.controller_errors import WrongTypeParameter


class CreateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_data: dict, case, requester_id) -> IUserRepository.create_user:
        new_user_data: dict = user_data.get('new_user');
    
        match case:
            case ROLE.ADM:
                # nome, email, organization; role
                try:

                    user = User(
                        user_id=f"{uuid.uuid4()}",
                        name=new_user_data.get('name'),
                        email=new_user_data.get('email'),
                        role=ROLE(new_user_data.get('role')),
                        organization=ORGANIZATION(new_user_data.get('organization')),
                        active=ACTIVE.ACTIVE,
                        state=STATE(new_user_data.get('state')) if new_user_data.get('state') else STATE.PENDING,
                        ra=re.search(r'(.+)@', new_user_data.get('email')).group(1)
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
                            name=new_user_data.get('name'),
                            email=new_user_data.get('email'),
                            role=ROLE.USER,
                            organization=ORGANIZATION(new_user_data.get('organization')),
                            course=COURSE(new_user_data.get('course')),
                            year=new_user_data.get('year'),
                            active=ACTIVE.ACTIVE,
                            state=STATE(new_user_data.get('state')) if new_user_data.get('state') else STATE.PENDING,
                            ra=re.search(r'(.+)@', new_user_data.get('email')).group(1)
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
                            name=new_user_data.get('name'),
                            email=new_user_data.get('email'),
                            role=ROLE(new_user_data.get('role')),
                            organization=ORGANIZATION(new_user_data.get('organization')),
                            active=ACTIVE.ACTIVE,
                            state=STATE(new_user_data.get('state')) if new_user_data.get('state') else STATE.PENDING,
                            ra=re.search(r'(.+)@', new_user_data.get('email')).group(1)
                        )

                        self.repo.has_permission_target_user(requester_id=requester_id, target_user=user)
                    except Exception as e:
                        raise e
                    
                    created_user = self.repo.create_user(new_user=user)
                    created_users.append(created_user)
                
                return created_users