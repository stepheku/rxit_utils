from pyramid.view import view_config
from rxit_utils.infrastructure import cookie_auth
from rxit_utils.view_models.shared.view_model_base import ViewModelBase

@view_config(route_name='home', renderer="rxit_utils:templates/home_index.pt")
def home_index(request):
    view_model = ViewModelBase(request)
    return view_model.to_dict()