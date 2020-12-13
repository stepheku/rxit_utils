from pyramid.request import Request
from rxit_utils.view_models.shared.view_model_base import ViewModelBase
from rxit_utils.services import user_service

class HomeViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)