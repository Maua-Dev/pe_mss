from src.modules.update_warning.app.update_warning_usecase import UpdateWarningUsecase
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse


class UpdateWarningController:
    def __init__(self, usecase: UpdateWarningUsecase):
        self.usecase= usecase

    def __call__(self, request: IRequest) -> IResponse:
        warning_id = request.data.get('warning_id')

        title = request.data.get('title')
        description = request.data.get('description')
        expire = request.data.get('expire')
        target_role = request.data.get('target_role')
        target_org = request.data.get('target_org')

        requester_user = request.data.get('user_from_authorizer')
        requester_user_id = requester_user.get('id') if requester_user else None

        updated_warning = self.usecase(
            warning_id=warning_id,
            title=title,
            description=description,
            expire=expire,
            target_role=target_role,
            user_id=requester_user_id,
            target_org=target_org
        )

        return updated_warning