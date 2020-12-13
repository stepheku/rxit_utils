from pyramid.request import Request
from rxit_utils.view_models.shared.view_model_base import ViewModelBase
from rxit_utils.services import user_service

class AccountHomeViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.user = user_service.find_user_by_id(self.user_id)