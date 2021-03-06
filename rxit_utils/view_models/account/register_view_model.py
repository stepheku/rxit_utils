from pyramid.request import Request
from rxit_utils.view_models.shared.view_model_base import ViewModelBase
from rxit_utils.services import user_service

class RegisterViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.username = self.request_dict.get("username")
        self.email = self.request_dict.get("email")
        self.password = self.request_dict.get("password")
        self.error = None
    
    def validate(self):
        if not self.username:
            self.error = "You must specify a username"
        elif not self.email:
            self.error = "You must specify an e-mail address"
        elif not self.password:
            self.error = "You must specify a password"
        elif user_service.find_user_by_username(username=self.username):
            self.error = "Username already exists"