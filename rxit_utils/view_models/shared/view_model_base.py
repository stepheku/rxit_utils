from pyramid.request import Request
from rxit_utils.infrastructure import cookie_auth
from rxit_utils.infrastructure import request_dict

class ViewModelBase:
    def __init__(self, request: Request):
        self.request = request
        self.request_dict = request_dict.create(request)
        self.error: str = None
        self.user_id = cookie_auth.get_user_id_via_auth_cookie(request=request)

    def to_dict(self):
        return self.__dict__