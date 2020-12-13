from pyramid.view import view_config
from pyramid import httpexceptions
from pyramid.request import Request
from rxit_utils.services import user_service
from rxit_utils.infrastructure import cookie_auth
from rxit_utils.view_models.account.account_home_view_model import AccountHomeViewModel
from rxit_utils.view_models.account.register_view_model import RegisterViewModel
from rxit_utils.view_models.account.login_view_model import LoginViewModel

# ################### INDEX #################################


@view_config(
    route_name="account_home", renderer="rxit_utils:templates/account/index.pt"
)
def index(request):
    view_model = AccountHomeViewModel(request)
    if not view_model.user:
        return httpexceptions.HTTPFound("/account/login")

    return view_model.to_dict()


# ################### LOGIN #################################


@view_config(
    route_name="login",
    renderer="rxit_utils:templates/account/login.pt",
    request_method="GET",
)
def login_get(request):
    view_model = LoginViewModel(request)
    return view_model.to_dict()


@view_config(
    route_name="login",
    renderer="rxit_utils:templates/account/login.pt",
    request_method="POST",
)
def login_post(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = user_service.login_user(username, password)

    if not user:
        error = "User not found or password incorrect"
        return {"username": username, "password": password, "error": error}

    cookie_auth.set_auth(request=request, user_id=user.id)

    return httpexceptions.HTTPFound("/account")


# ################### REGISTRATION ############################


@view_config(
    route_name="register",
    renderer="rxit_utils:templates/account/register.pt",
    request_method="GET",
)
def register_get(request):
    view_model = RegisterViewModel(request)
    return view_model.to_dict()


@view_config(
    route_name="register",
    renderer="rxit_utils:templates/account/register.pt",
    request_method="POST",
)
def register_post(request: Request):
    view_model = RegisterViewModel(request)
    view_model.validate()

    if view_model.error:
        return view_model.to_dict()

    # create user
    user = user_service.create_user(
        username=view_model.username,
        email=view_model.email,
        password=view_model.password,
    )

    if not user:
        view_model.error = "Registration failed"
        return view_model.to_dict()

    # user_id needs user.id and not from the view_model because
    # view_model.user_id has not yet been set
    cookie_auth.set_auth(request=request, user_id=user.id)

    return httpexceptions.HTTPFound("/account")


# ################### LOGOUT ############################


@view_config(route_name="logout")
def logout(request):

    cookie_auth.logout(request=request)

    return httpexceptions.HTTPFound("/")