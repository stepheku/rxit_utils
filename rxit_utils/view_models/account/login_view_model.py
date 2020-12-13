from pyramid.request import Request
from rxit_utils.view_models.shared.view_model_base import ViewModelBase

class LoginViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.username = None
        self.password = None
        self.error = None