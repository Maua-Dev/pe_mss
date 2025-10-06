from abc import ABC, abstractmethod
from typing import *
from src.shared.domain.entities.warning import Warning
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.enums.role_enum import ROLE


class IWarningRepository(ABC):
    
    #creation
    
    @abstractmethod
    def create_warning(self, new_warning: Warning, target_id: str, target_role: ROLE) -> Optional[Warning]:
        """ 
        Método que cria um aviso no banco de dados

        Args:
            new_warning (Warning): novo aviso a ser criado, passado como entidade
        Returns:
            Optional[Warning]: caso o aviso não seja um duplicado, retorna o aviso
        """
        pass
    
    # @abstractmethod
    # def link_to_users(self, warning_id: str, user_ids: list[str]) -> None:
    #     """
    #     Método que vincula um aviso à usuários pelo user_id

    #     Args:
    #         warning_id (str): id do aviso
    #         user_ids (list[str]): ids dos usuários a linkar
    #     """
        
    # @abstractmethod
    # def link_to_roles(self, warning_id: str, roles: list[ROLE]) -> None:
    #     """
    #     Método que vincula um aviso à roles

    #     Args:
    #         warning_id (str): id do aviso
    #         roles (list[ROLE]): roles que irão conter o aviso
    #     """
    
    #updates
    
    @abstractmethod
    def update_warning(self, warning_id: str, warning: Warning) -> Optional[Warning]:
        """
        Método que atualiza um aviso

        Args:
            warning_id (str): id do aviso a ser atualizado
            warning (str): objeto a ser atualizado

        Returns:
            Optional[Warning]: caso o alerta exista, retorna o alerta atualizado
        """
        
    #deletes
    
    @abstractmethod
    def delete_warning(self, warning_id: str, organization: ORGANIZATION) -> Optional[Warning]:
        """
        Método que delete um alerta

        Args:
            warning_id (str): id do alerta a ser deletado
            organization (ORGANIZATION): organização do alerta a ser deletado

        Returns:
            Optional[Warning]: caso o alerta exista e seja deletado, retorna o alerta
        """
    
    #getters
    
    @abstractmethod
    def get_warning(self, warning_id: str, target_org: ORGANIZATION) -> Optional[Warning]:
        """
        Método para buscar um aviso no banco por seu id

        Args:
            warning_id (str): id do aviso
            target_org (ORGANIZATION): organização do aviso a ser buscado

        Returns:
            Optional[Warning]: retorna um aviso caso encontre-o
        """
        pass
        
    @abstractmethod
    def get_all_warnings(self) -> Optional[List[Warning]]:
        """
        Método para pegar todos os avisos

        Returns:
            Optional[List[Warning]]: Uma lista de avisos caso haja avisos
        """
        pass
        
    # @abstractmethod
    # def get_user_warnings(self, user_id: str) -> Optional[List[Warning]]:
    #     """
    #     Método para pegar todos os avisos de um usuário
    #     Usa a tabela aviso_usuário

    #     Args:
    #         user_id (str): Id do usuário para buscar os avisos

    #     Returns:
    #         Optional[List[Warning]]: Uma lista de avisos caso haja avisos
    #     """
    #     pass
        
    # @abstractmethod
    # def get_president_warnings(self) -> Optional[List[Warning]]:
    #     """
    #     Método pra pegar os warnings direcionados aos presidentes
    #     Usa a tabela aviso_usuário

    #     Returns:
    #         Optional[List[Warning]]: Uma lista de avisos caso haja avisos
    #     """
    #     pass